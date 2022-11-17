# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class HrPayslipInputTypeInherit(models.Model):
    _inherit = "hr.payslip.input.type"

    generate = fields.Boolean(default=False, string="Generate")
