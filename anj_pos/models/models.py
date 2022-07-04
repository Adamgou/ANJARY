from odoo import fields, models, api


class ProdcutTemplaceInherit(models.Model):
    _inherit = "product.template"

    available_in_pos = fields.Boolean(
        string="Available in POS",
        help="Check if you want this product to appear in the Point of Sale.",
        default=True,
    )
