# coding: utf-8

from odoo import models, fields, api


class Account_invoice_line(models.Model):
    _inherit = "account.move.line"

    unit_price_discounted = fields.Float(
        "Prix unitaire remisé", compute="_compute_u_p_disc"
    )
    price_unit_ht = fields.Float(
        "Price HT", required=False, default=0.0, compute="compute_price_HT"
    )

    @api.depends("price_unit", "discount")
    def _compute_u_p_disc(self):
        for rec in self:
            rec.unit_price_discounted = rec.price_unit - (
                (rec.price_unit * rec.discount) / 100
            )

    @api.depends("product_id.list_price", "product_id.taxes_id")
    def compute_price_HT(self):
        for rec in self:
            tax_rate = (
                rec.product_id.taxes_id.filtered(
                    lambda x: x.company_id == self.company_id
                ).amount
                / 100
            )
            rec.price_unit_ht = round(rec.product_id.list_price / (1 + tax_rate), 2)

    @api.onchange("price_unit", "discount")
    def _on_change_price_discounted(self):
        for val in self.with_context(check_move_validity=False):
            value = val.price_unit - ((val.price_unit * val.discount) / 100)
            val.unit_price_discounted = value
