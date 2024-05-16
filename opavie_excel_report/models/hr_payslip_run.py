# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'

    employer_bank_account = fields.Many2one(
        comodel_name='res.partner.bank',
        string='Employer bank account',
        domain="[('id', 'in', bank_account_ids)]")
    
    bank_account_ids = fields.One2many(
        'res.partner.bank',
        compute='_compute_bank_account_ids'
    )

    def action_generate_opavie_report(self):
        return self.env.ref('opavie_excel_report.action_opavie_report').report_action(self)

    @api.depends('company_id')
    def _compute_bank_account_ids(self):
        for record in self:
            if record.company_id.partner_id.bank_ids:
                record.bank_account_ids = record.company_id.partner_id.bank_ids.ids
            else:
                record.bank_account_ids = False