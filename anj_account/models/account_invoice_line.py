# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Account_invoice_line(models.Model):
    _inherit='account.move.line'

    unit_price_discounted = fields.Float('Prix unitaire remisé',compute='_get_unit_price_discounted',)

    
    @api.depends('discount')
    def _get_unit_price_discounted(self):
        for val in self:
            value=val.price_unit-((val.price_unit*val.discount)/100)
            val.unit_price_discounted=value