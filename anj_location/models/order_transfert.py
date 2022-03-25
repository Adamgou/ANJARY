# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Order_transfert(models.Model):
    _name="order.transfert"
    _rec_name="hotel_partner"

    hotel_partner = fields.Char(
        string='Partner hotel',
        required=False)

    transfert_date = fields.Date(
        string='Transfert date',
        required=False)
    fligth_company = fields.Char(
        string='Company operating the flight',
        required=False)