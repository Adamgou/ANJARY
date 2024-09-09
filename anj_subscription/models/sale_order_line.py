# coding: utf-8

from odoo import fields, models, api

 
class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    subscription_state = fields.Selection(
        related="order_id.subscription_state", store=True
    )

