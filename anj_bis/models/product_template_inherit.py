from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    spoon = fields.Boolean(string="Spoon", default=False)
    spoon_displayed = fields.Boolean(related="company_id.is_biskot")
