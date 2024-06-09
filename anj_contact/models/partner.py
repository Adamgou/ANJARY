# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Res_partner(models.Model):
    _inherit="res.partner"

    chatId = fields.Char(string="Whatsapp Chat ID")
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

    driver_id = fields.Many2one('hr.employee', string='Chauffeur attitré',store = True)
    product_id = fields.Many2one('product.template', string='Véhicule',store = True)
    best_room = fields.Char('Chambre préférée',store = True)
    customer_codes = fields.Char()

    city = fields.Char(compute='get_the_city_id', store=True)
    city_id = fields.Many2one('res.city', ondelete='restrict')

    @api.depends('city_id')
    def get_the_city_id(self):
        for rec in self:
            rec.city = rec.city_id.name
            rec.zip = rec.city_id.zip



    