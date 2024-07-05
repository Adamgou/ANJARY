# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Sale_order_line(models.Model):
    _inherit = "sale.order.line"

    # TODO for jara trade and jara distribution

    unit_price_discounted = fields.Float(
        "Prix unitaire remisé",
        store=True,
    )

    is_jara = fields.Boolean(compute='_compute_is_jara')

    @api.depends("product_id")
    def _compute_is_jara(self):
        for rec in self:
            rec.is_jara = rec.env.company.name.lower().startswith('jara') or rec.env.company.name.lower().startswith('societe immobiliere')

    @api.onchange("discount", "price_unit")
    def _change_discount(self):
        for val in self:
            value = val.price_unit - ((val.price_unit * val.discount) / 100)
            val.unit_price_discounted = value

    @api.onchange("unit_price_discounted")
    def _onchange_unit_price_discounted(self):
        for val in self:
            if val.product_id and (val.price_unit):
                val.discount = ((val.price_unit - val.unit_price_discounted) * 100) / (
                    val.price_unit
                ) or 0
