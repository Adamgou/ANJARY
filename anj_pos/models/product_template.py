# coding: utf-8

from odoo import fields, models


class ProdcutTemplace(models.Model):
    _inherit = "product.template"
    
    related_biskot = fields.Boolean(related='company_id.is_biskot')
    available_in_pos = fields.Boolean(
        string="Available in POS",
        help="Check if you want this product to appear in the Point of Sale.",
        default=True,
    ) # do we really need this??? 
    available_in_tsaralalana = fields.Boolean(
        string="Available in TSARALALANA",
        help="Check if you want this product to appear in the Point of Sale.",
        default=False,
    ) 
    available_in_ivato = fields.Boolean(
        string="Available in IVAT0",
        help="Check if you want this product to appear in the Point of Sale.",
        default=False,
    ) 
