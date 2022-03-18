from odoo import models, fields, api

class Product_template(models.Model):
    _inherit='product.template'

    location_price_id = fields.Many2one(
        comodel_name='location.price',
        string='Location price',
        required=True)