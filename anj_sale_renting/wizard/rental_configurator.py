# coding: utf-8

import math
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

LOCATION_INTERVAL = {
    "journey": (5, 15),
    "evening": (15, 21),
    "night": (15, 2),
}


class RentalWizard(models.TransientModel):
    _name = "rental.wizard"
    _description = "Configure the rental of a product"

    def _default_uom_id(self):
        if self.env.context.get("default_uom_id", False):
            return self.env["uom.uom"].browse(self.context.get("default_uom_id"))
        else:
            return (
                self.env["product.product"]
                .browse(self.env.context.get("default_product_id"))
                .uom_id
            )

    rental_order_line_id = fields.Many2one(
        "sale.order.line", ondelete="cascade"
    )  # When wizard used to edit a Rental SO line

    product_id = fields.Many2one(
        "product.product",
        "Product",
        required=True,
        ondelete="cascade",
        domain=[("rent_ok", "=", True)],
        help="Product to rent (has to be rentable)",
    )
    uom_id = fields.Many2one(
        "uom.uom", "Unit of Measure", readonly=True, default=_default_uom_id
    )
    company_id = fields.Many2one(
        "res.company", default=lambda self: self.env.company.id, store=False
    )

    pickup_date = fields.Datetime(
        string="Pickup",
        required=True,
        default=lambda s: fields.Datetime.now().replace(
            hour=8, minute=0, second=0, microsecond=0
        ),
    )
    return_date = fields.Datetime(
        string="Return",
        required=True,
        default=lambda s: fields.Datetime.now().replace(
            hour=17, minute=0, second=0, microsecond=0
        ),
    )

    quantity = fields.Float(
        "Quantity", default=1, required=True, digits="Product Unit of Measure"
    )  # Can be changed on SO line later if needed

    pricing_id = fields.Many2one(
        "product.pricing",
        compute="_compute_pricing",
        string="Pricing",
        help="Best Pricing Rule based on duration",
    )
    currency_id = fields.Many2one(
        "res.currency", string="Currency", compute="_compute_currency_id"
    )

    duration = fields.Integer(
        string="Duration",
        compute="_compute_duration",
        help="The duration unit is based on the unit of the rental pricing rule.",
    )
    duration_unit = fields.Selection(
        [
            ("hour", "Hours"),
            ("day", "Days"),
            ("week", "Weeks"),
            ("month", "Months"),
            ("year", "Years"),
        ],
        string="Unit",
        required=True,
        compute="_compute_duration",
    )

    unit_price = fields.Monetary(
        string="Unit Price",
        help="This price is based on the rental price rule that gives the cheapest price for requested duration.",
        readonly=False,
        default=0.0,
        required=True,
    )
    pricelist_id = fields.Many2one("product.pricelist", string="Pricelist")

    pricing_explanation = fields.Html(
        string="Price Computation",
        help="Helper text to understand rental price computation.",
        compute="_compute_pricing_explanation",
    )

    location_price_id = fields.Many2one(
        comodel_name="location.price",
        string="Prix de location",
        store=True,
        required=True,
    )

    location_price = fields.Float(string="Montant", store=True, readonly=True)

    @api.depends("pickup_date", "return_date")
    def _compute_pricing(self):
        self.pricing_id = False
        for wizard in self:
            if wizard.product_id:
                company = wizard.company_id or wizard.env.company
                wizard.pricing_id = wizard.product_id._get_best_pricing_rule(
                    start_date=wizard.pickup_date,
                    end_date=wizard.return_date,
                    pricelist=wizard.pricelist_id,
                    company=company,
                    currency=wizard.currency_id or company.currency_id,
                )

    @api.depends("pricelist_id")
    def _compute_currency_id(self):
        for wizard in self:
            wizard.currency_id = (
                wizard.pricelist_id.currency_id or wizard.env.company.currency_id
            )

    @api.depends("pricing_id", "pickup_date", "return_date")
    def _compute_duration(self):
        for wizard in self:
            values = {
                "duration_unit": "day",
                "duration": 1.0,
            }
            if wizard.pickup_date and wizard.return_date:
                duration_dict = self.env["product.pricing"]._compute_duration_vals(
                    wizard.pickup_date, wizard.return_date
                )
                if wizard.pricing_id:
                    values = {
                        "duration_unit": wizard.pricing_id.recurrence_id.unit,
                        "duration": duration_dict[wizard.pricing_id.recurrence_id.unit],
                    }
                else:
                    values = {"duration_unit": "day", "duration": duration_dict["day"]}
            wizard.update(values)

    @api.onchange("pricing_id", "currency_id", "duration", "duration_unit")
    def _compute_unit_price(self):
        for wizard in self:
            if wizard.pricelist_id:
                wizard.unit_price = wizard.pricelist_id._get_product_price(
                    wizard.product_id,
                    1,
                    start_date=wizard.pickup_date,
                    end_date=wizard.return_date,
                )
            elif wizard.pricing_id and wizard.duration > 0:
                unit_price = wizard.pricing_id._compute_price(
                    wizard.duration, wizard.duration_unit
                )
                if wizard.currency_id != wizard.pricing_id.currency_id:
                    wizard.unit_price = wizard.pricing_id.currency_id._convert(
                        from_amount=unit_price,
                        to_currency=wizard.currency_id,
                        company=wizard.company_id,
                        date=fields.Date.today(),
                    )
                else:
                    wizard.unit_price = unit_price
            elif wizard.duration > 0:
                wizard.unit_price = wizard.product_id.lst_price

            product_taxes = wizard.product_id.taxes_id.filtered(
                lambda tax: tax.company_id.id == wizard.company_id.id
            )
            if wizard.rental_order_line_id:
                product_taxes_after_fp = wizard.rental_order_line_id.tax_id
            elif "sale_order_line_tax_ids" in self.env.context:
                product_taxes_after_fp = self.env["account.tax"].browse(
                    self.env.context["sale_order_line_tax_ids"] or []
                )
            else:
                product_taxes_after_fp = product_taxes

            # TODO : switch to _get_tax_included_unit_price() when it allow the usage of taxes_after_fpos instead
            # of fiscal position. We cannot currently use the fpos because JS only has access to the line information
            # when opening the wizard.
            product_unit_price = wizard.unit_price
            if set(product_taxes.ids) != set(product_taxes_after_fp.ids):
                flattened_taxes_before_fp = (
                    product_taxes._origin.flatten_taxes_hierarchy()
                )
                if any(tax.price_include for tax in flattened_taxes_before_fp):
                    taxes_res = flattened_taxes_before_fp.compute_all(
                        product_unit_price,
                        quantity=wizard.quantity,
                        currency=wizard.currency_id,
                        product=wizard.product_id,
                    )
                    product_unit_price = taxes_res["total_excluded"]

                flattened_taxes_after_fp = (
                    product_taxes_after_fp._origin.flatten_taxes_hierarchy()
                )
                if any(tax.price_include for tax in flattened_taxes_after_fp):
                    taxes_res = flattened_taxes_after_fp.compute_all(
                        product_unit_price,
                        quantity=wizard.quantity,
                        currency=wizard.currency_id,
                        product=wizard.product_id,
                        handle_price_include=False,
                    )
                    for tax_res in taxes_res["taxes"]:
                        tax = self.env["account.tax"].browse(tax_res["id"])
                        if tax.price_include:
                            product_unit_price += tax_res["amount"]
                wizard.unit_price = product_unit_price

    @api.depends("unit_price", "pricing_id")
    def _compute_pricing_explanation(self):
        translated_pricing_duration_unit = dict()
        for key, value in self.pricing_id.recurrence_id._fields[
            "unit"
        ]._description_selection(self.env):
            translated_pricing_duration_unit[key] = value
        for wizard in self:
            if wizard.pricing_id and wizard.duration > 0 and wizard.unit_price != 0.0:
                if wizard.pricing_id.recurrence_id.duration > 0:
                    pricing_explanation = "%i * %i %s (%s)" % (
                        math.ceil(
                            wizard.duration / wizard.pricing_id.recurrence_id.duration
                        ),
                        wizard.pricing_id.recurrence_id.duration,
                        translated_pricing_duration_unit[
                            wizard.pricing_id.recurrence_id.unit
                        ],
                        self.env["ir.qweb.field.monetary"].value_to_html(
                            wizard.pricing_id.price,
                            {
                                "from_currency": wizard.pricing_id.currency_id,
                                "display_currency": wizard.currency_id,
                                "company_id": self.env.company.id,
                            },
                        ),
                    )
                else:
                    pricing_explanation = _("Fixed rental price")
                if wizard.product_id.extra_hourly or wizard.product_id.extra_daily:
                    pricing_explanation += "<br/>%s" % (_("Extras:"))
                if wizard.product_id.extra_hourly:
                    pricing_explanation += " %s%s" % (
                        self.env["ir.qweb.field.monetary"].value_to_html(
                            wizard.product_id.extra_hourly,
                            {
                                "from_currency": wizard.product_id.currency_id,
                                "display_currency": wizard.currency_id,
                                "company_id": self.env.company.id,
                            },
                        ),
                        _("/hour"),
                    )
                if wizard.product_id.extra_daily:
                    pricing_explanation += " %s%s" % (
                        self.env["ir.qweb.field.monetary"].value_to_html(
                            wizard.product_id.extra_daily,
                            {
                                "from_currency": wizard.product_id.currency_id,
                                "display_currency": wizard.currency_id,
                                "company_id": self.env.company.id,
                            },
                        ),
                        _("/day"),
                    )
                wizard.pricing_explanation = pricing_explanation
            else:
                # if no pricing on product: explain only sales price is applied ?
                if not wizard.product_id.product_pricing_ids and wizard.duration:
                    wizard.pricing_explanation = _(
                        "No rental price is defined on the product.\nThe price used is the sales price."
                    )
                else:
                    wizard.pricing_explanation = ""

    _sql_constraints = [
        (
            "rental_period_coherence",
            "CHECK(pickup_date < return_date)",
            "Please choose a return date that is after the pickup date.",
        ),
    ]

    @api.onchange("location_price_id")
    def _onchange_location_price_id(self):
        if self.location_price_id:
            if (
                self.location_price_id.id
                == self.env.ref("anj_sale_renting.journey_price").id
            ):
                location_interval = LOCATION_INTERVAL.get("journey")
            elif (
                self.location_price_id.id
                == self.env.ref("anj_sale_renting.evening_price").id
            ):
                location_interval = LOCATION_INTERVAL.get("evening")
            else:
                location_interval = LOCATION_INTERVAL.get("night")
            location_hours = abs(location_interval[1] - location_interval[0])
            self.pickup_date = self.pickup_date.replace(
                hour=location_interval[0], minute=0, second=0, microsecond=0
            )

            self.return_date = self.pickup_date + timedelta(hours=location_hours)

    @api.onchange("location_price_id", "quantity", "pickup_date", "return_date")
    def onchange_location_price_id(self):
        for data in self:
            data.unit_price = data.location_price_id.location_price
            data.location_price = data.location_price_id.location_price

    def get_location_price(self):
        return self.location_price_id.id

    def get_sale_order_line_multiline_description_sale(self, product):
        """Add Rental information to the SaleOrderLine name."""
        return self.get_location_price(product)

    warehouse_id = fields.Many2one("stock.warehouse", string="Warehouse")

    product_uom_id = fields.Char(string="Product UoM", related="product_id.uom_id.name")

    # Stock availability
    rented_qty_during_period = fields.Float(
        string="Quantity reserved",
        help="Quantity reserved by other Rental lines during the given period",
        compute="_compute_rented_during_period",
    )
    rentable_qty = fields.Float(
        string="Quantity available in stock for given period",
        compute="_compute_rentable_qty",
    )

    # Serial number management (lots are disabled for Rental Products)
    tracking = fields.Selection(related="product_id.tracking")
    lot_ids = fields.Many2many(
        "stock.lot",
        string="Serial Numbers",
        help="Only available serial numbers are suggested.",
        domain="[(qty_available_during_period > 0, '=', 1), ('id', 'not in', rented_lot_ids), ('id', 'in', rentable_lot_ids)]"
    )
    rentable_lot_ids = fields.Many2many(
        "stock.lot",
        string="Serials available in Stock",
        compute="_compute_rentable_lots",
    )
    rented_lot_ids = fields.Many2many(
        "stock.lot",
        string="Serials in rent for given period",
        compute="_compute_rented_during_period",
    )

    # Rental Availability
    qty_available_during_period = fields.Float(
        string="Quantity available for given period (Stock - In Rent)",
        compute="_compute_rental_availability",
        digits="Product Unit of Measure",
    )

    is_product_storable = fields.Boolean(compute="_compute_is_product_storable")

    @api.depends("pickup_date", "return_date", "product_id", "warehouse_id")
    def _compute_rented_during_period(self):
        for rent in self:
            if not rent.product_id or not rent.pickup_date or not rent.return_date:
                rent.rented_qty_during_period = 0.0
                rent.rented_lot_ids = False
                return
            fro, to = rent.product_id._unavailability_period(
                rent.pickup_date, rent.return_date
            )
            if rent.tracking != "serial":
                rent.rented_qty_during_period = rent.product_id._get_unavailable_qty(
                    fro,
                    to,
                    ignored_soline_id=rent.rental_order_line_id
                    and rent.rental_order_line_id.id,
                    warehouse_id=rent.warehouse_id.id,
                )
                rent.rented_lot_ids = False
            else:
                rented_qty, rented_lots = rent.product_id._get_unavailable_qty_and_lots(
                    fro,
                    to,
                    ignored_soline_id=rent.rental_order_line_id
                    and rent.rental_order_line_id.id,
                    warehouse_id=rent.warehouse_id.id,
                )

                rent.rented_qty_during_period = rented_qty
                rent.rented_lot_ids = rented_lots

    @api.depends("pickup_date", "return_date", "product_id", "warehouse_id")
    def _compute_rentable_qty(self):
        for rent in self:
            if rent.is_product_storable and rent.pickup_date and rent.return_date:
                reservation_begin, reservation_end = (
                    rent.product_id._unavailability_period(
                        rent.pickup_date, rent.return_date
                    )
                )
                rent.rentable_qty = rent.product_id.with_context(
                    from_date=max(reservation_begin, fields.Datetime.now()),
                    to_date=reservation_end,
                    warehouse=rent.warehouse_id.id,
                ).qty_available
                if reservation_begin > fields.Datetime.now():
                    # Available qty at period t = available stock now + qty in rent now.
                    rent.rentable_qty += rent.product_id.with_context(
                        warehouse_id=rent.warehouse_id.id
                    ).qty_in_rent
            else:
                rent.rentable_qty = 0

    @api.depends("product_id", "warehouse_id")
    def _compute_rentable_lots(self):
        for rent in self:
            if rent.product_id and rent.tracking == "serial":
                rentable_lots = self.env["stock.lot"]._get_available_lots(
                    rent.product_id, rent.warehouse_id.lot_stock_id
                )
                domain = [
                    ("is_rental", "=", True),
                    ("product_id", "=", rent.product_id.id),
                    ("order_id.rental_status", "in", ["pickup", "return"]),
                    ("state", "in", ["sale", "done"]),
                    ("id", "!=", rent.rental_order_line_id.id),
                ]
                if rent.warehouse_id:
                    domain += [("order_id.warehouse_id", "=", rent.warehouse_id.id)]
                # Total of lots = lots available + lots currently picked-up.
                rentable_lots += (
                    self.env["sale.order.line"]
                    .search(domain)
                    .mapped("pickedup_lot_ids")
                )
                rent.rentable_lot_ids = rentable_lots
            else:
                rent.rentable_lot_ids = self.env["stock.lot"]

    @api.depends("quantity", "rentable_qty", "rented_qty_during_period")
    def _compute_rental_availability(self):
        for rent in self:
            rent.qty_available_during_period = max(
                rent.rentable_qty - rent.rented_qty_during_period, 0
            )

    @api.depends("product_id")
    def _compute_is_product_storable(self):
        """Product type ?= storable product."""
        for rent in self:
            rent.is_product_storable = (
                rent.product_id and rent.product_id.type == "product"
            )

    @api.onchange("lot_ids")
    def _onchange_lot_ids(self):
        if self.tracking == "serial" and self.lot_ids:
            self.quantity = len(self.lot_ids)

    @api.onchange("quantity")
    def _onchange_qty(self):
        """Remove last lots when qty is decreased."""
        if len(self.lot_ids) > self.quantity:
            self.lot_ids = self.lot_ids[: int(self.quantity)]

    @api.onchange("product_id")
    def _onchange_product_id(self):
        if self.lot_ids and self.lot_ids.mapped("product_id") != self.product_id:
            self.lot_ids = self.env["stock.lot"]

    @api.constrains("product_id", "rental_order_line_id")
    def _pickedup_product_no_change(self):
        for wizard in self:
            if (
                wizard.rental_order_line_id
                and wizard.product_id != wizard.rental_order_line_id.product_id
                and wizard.rental_order_line_id.qty_delivered > 0
            ):
                raise ValidationError(
                    _("You cannot change the product of a picked-up line.")
                )
