# coding: utf-8

import calendar
from dateutil.relativedelta import relativedelta

from odoo import models, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _prepare_invoice_line(self, **optional_values):
        res = super()._prepare_invoice_line(**optional_values)
        if (
            self.order_id.is_subscription
            and self.order_id.prorata
            and self.order_id.plan_id.billing_period_unit == "month"
        ):
            res.update(
                {
                    "quantity": self._get_quantity_prorata(
                        res.get("quantity"),
                        self.order_id.start_date,
                        self.order_id.next_invoice_date - relativedelta(days=1),
                    )
                }
            )
        return res

    @api.model
    def _get_quantity_prorata(self, quantity, date_from, date_to):
        output = quantity
        if date_from.month == date_to.month and date_from.year == date_to.year:
            number_of_days = (date_to - date_from).days + 1
            month_range = calendar.monthrange(date_to.year, date_from.month)[1]
            if number_of_days != month_range:
                output = (number_of_days / month_range) + (
                    quantity - 1 if quantity > 0 else quantity
                )
        return output
