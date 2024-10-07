# coding: utf-8

from odoo import api, fields, models, _
from odoo.tools import format_amount


class ProductTemplate(models.Model): 
    _inherit = "product.template"

    price_unit_ht = fields.Float(
        "Sale Price HT", required=False, default=0.0, compute="compute_price_HT"
    )

    @api.depends("list_price", "taxes_id")
    def compute_price_HT(self):
        for rec in self:
            tax_rate = (
                rec.taxes_id.filtered(lambda x: x.company_id == self.company_id).amount
                / 100
            )
            rec.price_unit_ht = round(rec.list_price / (1 + tax_rate), 2)
