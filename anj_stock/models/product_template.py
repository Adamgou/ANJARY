from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = ["multi.company.abstract", "product.template"]
    _name = "product.template"
    _description = "Product Template (Multi-Company)"