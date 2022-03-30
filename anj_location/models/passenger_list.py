# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

class Passenger(models.Model):
    _name='passenger.list.praxi'
    name = fields.Char('Name')
    passenger_sale_order_id = fields.Many2one('sale.order', string='Order Transfert')
    cin = fields.Char('CIN')
    age = fields.Integer('Age')
    
    number_passenger = fields.Integer(
        string='Number of Passenger',
    )

    hotel = fields.Char('Hotel')