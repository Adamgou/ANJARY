# -*- coding: utf-8 -*-

from termios import CINTR
from odoo import models, fields, api


class Hr_employee(models.Model):
    _inherit = 'hr.employee'
    cnaps = fields.Char('CNAPS')
    ostie = fields.Char('OSTIE')
    cin = fields.Char('CIN')
    matricule = fields.Char('Matricule')
    classification = fields.Selection([
        ('hc', 'HC'),
        ('op', 'OP'),
        ('etc', 'Etc'),
    ], string='Classification')


class HrEmployeePublic(models.Model):
    _inherit = 'hr.employee.public'
    cnaps = fields.Char(readonly=True)
    ostie = fields.Char(readonly=True)
    cin = fields.Char(readonly=True)
    matricule = fields.Char(readonly=True)
    classification = fields.Selection([
        ('hc', 'HC'),
        ('op', 'OP'),
        ('etc', 'Etc'),
    ], string='Classification', readonly=True)
