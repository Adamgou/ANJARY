# coding: utf-8

from odoo.exceptions import UserError

from odoo import models, _


class SaleSubscription(models.Model):
    _inherit = "sale.order"

    def _confirm_subscription(self):
        res = super()._confirm_subscription()

        product_busy = self.env["sale.order.line"].search(
            [
                ("subscription_state", "=", "3_progress"),
                ("product_id", "in", self.order_line.mapped("product_id").ids),
                ("order_id", "!=", self.id),
                ("is_renewing", "=", False),
            ]
        )

        if product_busy:
            raise UserError(
                _("Busy real estate: {}").format(
                    ",".join(product_busy.mapped("name"))
                )
            )

        return res
