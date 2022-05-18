# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Sale_order_line(models.Model):
    _inherit='sale.order.line'

    # TODO for jara trade and jara distribution

    unit_price_discounted = fields.Float('Prix unitaire remisé',store=True)

    @api.onchange('discount')
    def _onchange_discount(self):
        for val in self:
            value=val.price_unit-((val.price_unit*val.discount)/100)
            val.unit_price_discounted=value

    @api.onchange('unit_price_discounted')
    def _onchange_unit_price_discounted(self):
        for val in self:
            val.discount=((val.price_unit - val.unit_price_discounted ) * 100) / (val.price_unit) or 0

