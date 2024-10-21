# coding: utf-8

from datetime import timedelta

import pytz

from odoo import models, fields, api, _
from odoo.osv.expression import AND


class ReportSaleDetails(models.AbstractModel):
    _inherit = "report.point_of_sale.report_saledetails"

    def _get_products_info_by_line_categ(self, line, products, product_id):
        """Get product info by line order and by category"""
        key1 = (
            line.product_id.product_tmpl_id.pos_categ_ids[0].name
            if len(line.product_id.product_tmpl_id.pos_categ_ids)
            else _("Not Categorized")
        )
        key2 = (product_id, line.price_unit)
        products.setdefault(key1, {})

        products[key1].setdefault(key2, [0.0, 0.0])
        products[key1][key2][0] += line.price_subtotal_incl - line.price_subtotal
        products[key1][key2][1] += line.price_subtotal_incl

        return products

    def _get_pos_order(
        self, date_start=False, date_stop=False, config_ids=False, session_ids=False
    ):
        """Get pos orders"""
        domain = [("state", "in", ["paid", "invoiced", "done"])]
        if session_ids:
            domain = AND([domain, [("session_id", "in", session_ids)]])
        else:
            if date_start:
                date_start = fields.Datetime.from_string(date_start)
            else:
                user_tz = pytz.timezone(
                    self.env.context.get("tz") or self.env.user.tz or "UTC"
                )
                today = user_tz.localize(
                    fields.Datetime.from_string(fields.Date.context_today(self))
                )
                date_start = today.astimezone(pytz.timezone("UTC")).replace(tzinfo=None)

            if date_stop:
                date_stop = fields.Datetime.from_string(date_stop)
                if date_stop < date_start:
                    date_stop = date_start + timedelta(days=1, seconds=-1)
            else:
                date_stop = date_start + timedelta(days=1, seconds=-1)

            domain = AND(
                [
                    domain,
                    [
                        ("date_order", ">=", fields.Datetime.to_string(date_start)),
                        ("date_order", "<=", fields.Datetime.to_string(date_stop)),
                    ],
                ]
            )

            if config_ids:
                domain = AND([domain, [("config_id", "in", config_ids)]])

        orders = self.env["pos.order"].search(domain)
        return orders

    def _get_product_info_by_categ(self, line, product_info):
        """Get product info by category"""
        product_info = self._get_products_info_by_line_categ(
            line, product_info, line.product_id.id
        )
        return product_info

    def _get_amount_per_category(self, categories, product_amount_info, product_info):
        """Get amount by category"""
        product_ids = []
        for categ in categories:
            tax_amount = 0
            amount_incl_vat = 0
            products = categ.get("products")
            categ_name = categ.get("name")
            for product in products:
                product["tax_amount"] = 0
                product["amount_incl_vat"] = 0
                key = (product["product_id"], product["price_unit"])
                if (
                    categ_name in product_amount_info
                    and key in product_amount_info[categ_name]
                ):
                    product["tax_amount"] = product_amount_info[categ_name][key][0]
                    product["amount_incl_vat"] = product_amount_info[categ_name][key][1]
                tax_amount += product["tax_amount"]
                amount_incl_vat += product["amount_incl_vat"]
                product_ids.append(product.get("product_id"))
            categ["tax_amount"] = tax_amount
            categ["amount_incl_vat"] = amount_incl_vat

        unique_products = list(
            {
                tuple(sorted(product.items())): product
                for categ in categories
                for product in categ["products"]
            }.values()
        )
        product_info.update(
            {
                "all_tax_amount": sum(
                    product["tax_amount"] or 0 for product in unique_products
                ),
                "all_amount_incl_vat": sum(
                    product["amount_incl_vat"] or 0 for product in unique_products
                ),
            }
        )

        return categories, product_info, product_ids

    def _get_pos_info(self, date_start, date_stop, config_ids, session_ids):
        """
            Get pos info
        :param date_start:
        :param date_stop:
        :param config_ids:
        :param session_ids:
        :return: Dictionary of session and config
        """
        configs = []
        sessions = []
        pos_info = {}
        if config_ids:
            configs = self.env["pos.config"].search([("id", "in", config_ids)])
            if session_ids:
                sessions = self.env["pos.session"].search([("id", "in", session_ids)])
            else:
                sessions = self.env["pos.session"].search(
                    [
                        ("config_id", "in", configs.ids),
                        ("start_at", ">=", date_start),
                        ("stop_at", "<=", date_stop),
                    ]
                )
        else:
            sessions = self.env["pos.session"].search([("id", "in", session_ids)])
            for session in sessions:
                configs.append(session.config_id)
        pos_info.setdefault("session", sessions)
        pos_info.setdefault("config", configs)
        return pos_info

    def _get_default_payment(self):
        """Get default payment method dict"""
        payment_by_product = {}
        payment_by_product.setdefault("mvola", 0.0)
        payment_by_product.setdefault("CB", 0.0)
        return payment_by_product

    def _get_payment_by_method(self, payment_by_product, config_ids, sessions):
        """Get payment amount according payment method"""
        methods_configs = [
            method.id for config in config_ids for method in config.payment_method_ids
        ]
        domain = [
            ("payment_method_id", "in", methods_configs),
            ("session_id", "in", sessions.ids),
        ]
        mvola_payment = sum(
            payment.amount
            for payment in self.env["pos.payment"]
            .search(domain)
            .filtered(lambda l: l.payment_method_id.is_mvola)
        )
        cb_payment = sum(
            payment.amount
            for payment in self.env["pos.payment"]
            .search(domain)
            .filtered(lambda l: l.payment_method_id.is_cb)
        )
        payment_by_product["mvola"] = mvola_payment
        payment_by_product["CB"] = cb_payment
        return payment_by_product

    def _get_pricelist(self, configs):
        """
            Get client who needs checking expendses
        :return:
        """
        pricelists = []
        for config in configs:
            pricelists.extend(
                config.pricelist_id.ids + config.available_pricelist_ids.ids
            )
        product_pricelists = self.env["product.pricelist"].browse(pricelists)
        lists = {}
        for price in product_pricelists:
            lists.setdefault(price.id, {})
            lists[price.id].setdefault(price.name, 0.0)
        return lists

    def _get_pricelist_value(self, order, lists):
        """
                Get expenses of checking clients
        :param order:
        :param checking_clients:
        :return:
        """
        if order.pricelist_id:
            lists[order.pricelist_id.id][order.pricelist_id.name] += order.amount_paid
        return lists

    @api.model
    def get_sale_details(
        self, date_start=False, date_stop=False, config_ids=False, session_ids=False
    ):
        """Manage sale details for Biskot company case (Biskot and spoon product)"""
        out = super().get_sale_details(date_start, date_stop, config_ids, session_ids)
        orders = self._get_pos_order(date_start, date_stop, config_ids, session_ids)
        payments_method = self.env["pos.payment.method"].search(
            ["|", ("is_mvola", "=", True), ("is_cb", "=", True)]
        )
        product_amount_info = {}
        payments_by_method = self._get_default_payment()
        configs = self._get_pos_info(date_start, date_stop, config_ids, session_ids)[
            "config"
        ]
        sessions = self._get_pos_info(date_start, date_stop, config_ids, session_ids)[
            "session"
        ]

        pricelists = self._get_pricelist(configs)
        for order in orders:
            self._get_pricelist_value(order, pricelists)
            for line in order.lines:

                product_amount_info = self._get_product_info_by_categ(
                    line, product_amount_info
                )
        categories = out.get("products")
        product_info = out.get("products_info")
        categories, product_info, product_ids = self._get_amount_per_category(
            categories, product_amount_info, product_info
        )

        products = self.env["product.product"].search(
            [("id", "in", product_ids), ("spoon", "=", True)]
        )
        spoons = products.mapped("id")

        out.update({"spoons": spoons})

        spoons_data = []
        biskot_categories = []
        for categ in categories:
            removed = 0
            categ_products = categ.get("products")
            spoon_category = {
                "name": "",
                "qty": 0.0,
                "total": 0.0,
                "products": [],
                "tax_amount": 0.0,
                "amount_incl_vat": 0.0,
            }
            fake_products = categ_products.copy()
            for i, product in enumerate(fake_products):
                if product.get("product_id") in spoons:
                    spoon_category["name"] = categ.get("name")
                    spoon_category["products"].append({**product})
                    spoon_category["total"] += product.get("base_amount")
                    spoon_category["qty"] += product.get("quantity")
                    spoon_category["tax_amount"] += product.get("tax_amount")
                    spoon_category["amount_incl_vat"] += product.get("amount_incl_vat")
                    categ["qty"] -= product["quantity"]
                    categ["total"] -= product["base_amount"]
                    categ["tax_amount"] -= product["tax_amount"]
                    categ["amount_incl_vat"] -= product["amount_incl_vat"]
                    categ_products.pop(i - removed)
                    removed += 1
            if categ_products:
                biskot_categories.append(categ)
            if spoon_category.get("products"):
                spoons_data.append(spoon_category)

        payments_by_method = self._get_payment_by_method(
            payments_by_method, configs, sessions
        )
        out.update(
            {
                "spoons_data": spoons_data,
                "payments_by_method": payments_by_method,
                "payments_method": payments_method.filtered(
                    lambda l: l.config_ids in configs
                ),
                "pricelists": pricelists,
                "biskot_categories": biskot_categories,
            }
        )

        return out
