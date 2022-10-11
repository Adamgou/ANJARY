# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Account_invoice_line(models.Model):
    _inherit = "account.move.line"

    unit_price_discounted = fields.Float(
        "Prix unitaire remisé",
        store=True,
    )

    @api.onchange("price_unit", "discount")
    def _on_change_price_discounted(self):
        for val in self.with_context(check_move_validity=False):
            print(
                """ 
                    >>>
                    >>>
                    >>>
                """
            )
            value = val.price_unit - ((val.price_unit * val.discount) / 100)
            val.unit_price_discounted = value

    @api.model
    def create(self, vals):
        if vals.get("price_unit"):
            vals["unit_price_discounted"] = vals.get("price_unit")
        return super(Account_invoice_line, self).create(vals)