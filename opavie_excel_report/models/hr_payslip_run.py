# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'

    employer_bank_account = fields.Many2one(
        comodel_name='res.partner.bank',
        string='Employer bank account')

    def action_generate_opavie_report(self):
        return self.env.ref('opavie_excel_report.action_opavie_report').report_action(self)