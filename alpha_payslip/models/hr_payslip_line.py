# -*- coding: utf-8 -*-
from datetime import date

from odoo import fields, models, api

# from odoo.exceptions import UserError, Warning
# raise UserError(f"La date d'entrée ")


class HrPayslipLine(models.Model):
    _inherit = "hr.payslip.line"

    nombre = fields.Float(default=0, string="Nombre")
    base = fields.Float(default=0, string="Base")
