# coding: utf-8

from odoo import fields, models


class SaleOrderLine(models.Model):
    """Extend sale.order.line"""

    _inherit = "sale.order.line"

    subscription_state = fields.Selection(
        related="order_id.subscription_state", store=True
    )
    is_renewing = fields.Boolean(related="order_id.is_renewing", store=True)
