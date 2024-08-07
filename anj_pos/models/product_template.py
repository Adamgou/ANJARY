# coding: utf-8

from odoo import fields, models


class ProdcutTemplace(models.Model):
    _inherit = "product.template"
 
    available_in_pos = fields.Boolean(
        string="Available in POS",
        help="Check if you want this product to appear in the Point of Sale.",
        default=True,
    ) # do we really need this??? 
