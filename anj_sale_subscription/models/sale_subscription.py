# coding: utf-8

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


INTERVAL_FACTOR = {
    "daily": 30.0,
    "weekly": 30.0 / 7.0,
    "monthly": 1.0,
    "yearly": 1.0 / 12.0,
}

PERIODS = {"daily": "days", "weekly": "weeks", "monthly": "months", "yearly": "years"}


class SaleSubscription(models.Model):
    _inherit = "sale.order"

    prorata = fields.Boolean(default=True)
    is_monthly = fields.Boolean(compute="compute_is_monthly", store=True)
    can_read_move = fields.Boolean(
        default=lambda self: self.env["account.move"].check_access_rights(
            "read", raise_exception=False
        )
    )
    product_ids = fields.Many2many(
        comodel_name="product.product", compute="_compute_product_ids"
    )

    @api.depends("order_line.product_id")
    def _compute_product_ids(self):
        for rec in self:
            rec.product_ids = [(6, False, rec.order_line.mapped("product_id").ids)]

    @api.depends("plan_id.billing_period_unit")
    def compute_is_monthly(self):
        for sale_sub in self:
            sale_sub.is_monthly = sale_sub.plan_id.billing_period_unit == "month"

    def _compute_next_invoice_date(self):
        super()._compute_next_invoice_date()
        today = fields.Date.today()
        for sale_order in self:
            if (
                sale_order.prorata
                and sale_order.is_monthly
                and (today == self.start_date or today.day == 1)
            ):
                sale_order.next_invoice_date = today.replace(day=1) + relativedelta(
                    months=1
                )
