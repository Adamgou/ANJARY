# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Res_partner(models.Model):
    _inherit="res.partner"

    nif = fields.Char(
        string='NIF',
        required=False)
    stat = fields.Char(
        string='STAT',
        required=False)
    cif = fields.Char(
        string='CIF',
        required=False)
    rcs = fields.Char(
        string='RCS',
        required=False)