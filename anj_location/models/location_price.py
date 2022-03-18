from odoo import models, fields, api

class Location_price(models.Model):
    _name='location.price'
    _inherit = ['mail.thread']
    name = fields.Char(
        string='Name',
        required=False,track_visibility='onchange')

    location_price = fields.Float(
        string='Location price',
        required=False,track_visibility='onchange')