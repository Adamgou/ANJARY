# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Company(models.Model):
    _inherit = "res.company"

    nif = fields.Char("NIF", company_dependent=True)
    stat = fields.Char("STAT", company_dependent=True)
    cif = fields.Char("CIF", company_dependent=True)
    rcs = fields.Char(string='RCS', company_dependent=True)
    active = fields.Boolean('Active', default=True)
