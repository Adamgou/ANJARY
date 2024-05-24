# -*- coding:utf-8 -*-


from odoo import api, Command, fields, models, _


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    balance_to_date = fields.Float()
    balance_on_pay_slip = fields.Float()
    previous_paid_leave_balance = fields.Float()
    gain_on_current_month = fields.Selection([('0', '0'), ('2.5', '2,5')], default='2.5')
    days_taken_in_the_month = fields.Float(compute='compute_days_taken_in_the_month')
    new_balance_in_the_month = fields.Float(compute='_compute_new_balance_in_the_month')


    @api.model_create_multi
    def create(self, vals_list):
        res = super(HrPayslip, self).create(vals_list)
        for payslip in res:
            if payslip.employee_id and payslip.gain_on_current_month:
                payslip.balance_to_date = payslip.employee_id.leaves_count
                if payslip.gain_on_current_month == '2.5':
                    payslip.balance_on_pay_slip = payslip.employee_id.leaves_count + 2.5
                else:
                    payslip.balance_on_pay_slip = payslip.employee_id.leaves_count
        return res

    def write(self, vals):
        res = super(HrPayslip, self).write(vals)
        if 'gain_on_current_month' in vals and vals['gain_on_current_month']:
            for slip in self:
                if vals['gain_on_current_month'] == '2.5':
                    slip.balance_on_pay_slip = slip.balance_to_date + 2.5
                else:
                    slip.balance_on_pay_slip = slip.balance_to_date
        return res

    @api.onchange('employee_id')
    def set_balance_onchange_date(self):
        if self.env.user.has_group('smt_hr_payroll.group_can_modif_balance_payroll'):
            self.is_can_modif_all_balance = True
        else:
            self.is_can_modif_all_balance = False
        for paye in self:
            if paye.employee_id:
                last_payroll = self.env['hr.payslip'].search([
                    ('employee_id', '=', paye.employee_id.id),
                ], order='date_to desc', limit=1)

                if last_payroll:
                    paye.previous_paid_leave_balance = last_payroll.new_balance_in_the_month
                else:
                    paye.previous_paid_leave_balance = 0.0

    @api.onchange('employee_id')
    def get_balance_to_date(self):
        for paye in self:
            paye.balance_to_date = paye.employee_id.leaves_count
            if paye.gain_on_current_month == "2.5":
                paye.balance_on_pay_slip = paye.balance_to_date + 2.5
            elif paye.gain_on_current_month == "0":
                paye.balance_on_pay_slip = paye.balance_to_date

    @api.onchange('gain_on_current_month','employee_id')
    def change_gain_on_current_month(self):
        for paye in self:
            if paye.gain_on_current_month == "2.5":
                paye.balance_on_pay_slip = paye.balance_to_date + 2.5
            elif paye.gain_on_current_month == "0":
                paye.balance_on_pay_slip = paye.balance_to_date

    @api.onchange('previous_paid_leave_balance')
    def onchange_previous_paid_leave_balance(self):
        for paye in self:
            paye.new_balance_in_the_month = (paye.previous_paid_leave_balance + float(paye.gain_on_current_month)) - paye.days_taken_in_the_month


    def _compute_new_balance_in_the_month(self):
        for paye in self:
            paye.new_balance_in_the_month = (paye.previous_paid_leave_balance + float(paye.gain_on_current_month)) - paye.days_taken_in_the_month

    def compute_days_taken_in_the_month(self):
        for paye in self:
            paye.days_taken_in_the_month = sum(paye.worked_days_line_ids.filtered(lambda w: w.work_entry_type_id.code == 'LEAVE200').mapped('number_of_days'))
