# -*- coding: utf-8 -*-

from odoo import api, fields, models


class City(models.Model):
    _name = 'res.city'
    _description = 'City Partner'
    _order = 'name'

    name = fields.Char(string='City Name', required=True, translate=True, help='The full name of the city.')
    zip = fields.Char()