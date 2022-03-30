from odoo import models, fields, api

class Location_price(models.Model):
    _name='location.price'
    _description = 'location price '
    _inherit = ['mail.thread']
    name = fields.Char(
        string='Name',
        required=False)

    location_price = fields.Float(
        string='Location price',
        required=False)