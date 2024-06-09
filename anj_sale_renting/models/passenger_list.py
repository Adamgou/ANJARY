# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Passenger(models.Model):
    _name = "passenger.list.praxi"
    _description = "list of all passenger "

    name = fields.Char("Nom")
    passenger_sale_order_id = fields.Many2one("sale.order", string="Ordre de transfert")
    cin = fields.Char("CIN/Passeport")
    age = fields.Integer("Age")

    number_passenger = fields.Integer(
        string="Nombre de passager",
    )

    hotel = fields.Char("Hotel")


class Additive_passenger(models.Model):
    _name = "passenger.list.additive"
    _description = "list of all additive passenger "

    name = fields.Char("Nom")
    passenger_additive_sale_order_id = fields.Many2one(
        "sale.order", string="Ordre de transfert"
    )
    cin = fields.Char("CIN/Passeport")
    age = fields.Integer("Age")

    number_passenger = fields.Integer(
        string="Nombre de passager",
    )
