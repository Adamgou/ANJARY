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

    nickname = fields.Char('Surnom',company_dependent=True)

    driver_id = fields.Many2one('hr.employee', string='Chauffeur attitré')
    product_id = fields.Many2one('product.template', string='Véhicule')
    best_room = fields.Char('Chambre préférée')

    company_anj_id = fields.Many2one('res.company_id', string='Company Anj')

    