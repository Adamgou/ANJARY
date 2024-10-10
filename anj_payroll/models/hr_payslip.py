# coding: utf-8

from collections import defaultdict
from datetime import timedelta

from odoo import models, fields, api
from odoo.addons.resource.models.utils import HOURS_PER_DAY
from odoo.tools.date_utils import get_timedelta


class HRPayslip(models.Model):
	_inherit = "hr.payslip"
	
	payment_mode_id = fields.Many2one(comodel_name="hr.payslip.payment.mode")
	balance_to_date = fields.Float()
	gain_on_current_month = fields.Selection([('0', '0'), ('2.5', '2,5')], default='2.5')
	balance_on_pay_slip = fields.Float()
	is_can_modif_all_balance = fields.Boolean(compute='_compute_is_can_modif_all_balance')
	# previous_paid_leave_balance = fields.Float()
	previous_paid_leave_balance = fields.Float(compute="compute_previous_paid_leave_balance", store=True,
	                                           readonly=False)
	days_taken_in_the_month = fields.Float(compute='compute_days_taken_in_the_month')
	new_balance_in_the_month = fields.Float(compute='_compute_new_balance_in_the_month')
	
	def _compute_is_can_modif_all_balance(self):
		if self.env.user.has_group('smt_hr_payroll.group_can_modif_balance_payroll'):
			self.is_can_modif_all_balance = True
		else:
			self.is_can_modif_all_balance = False
	
	@api.model_create_multi
	def create(self, vals_list):
		res = super(HRPayslip, self).create(vals_list)
		for payslip in res:
			if payslip.employee_id and payslip.gain_on_current_month:
				payslip.balance_to_date = payslip.employee_id.leaves_count
				if payslip.gain_on_current_month == '2.5':
					payslip.balance_on_pay_slip = payslip.employee_id.leaves_count + 2.5
				else:
					payslip.balance_on_pay_slip = payslip.employee_id.leaves_count
		return res
	
	def write(self, vals):
		res = super(HRPayslip, self).write(vals)
		if 'gain_on_current_month' in vals and vals['gain_on_current_month']:
			for slip in self:
				if vals['gain_on_current_month'] == '2.5':
					slip.balance_on_pay_slip = slip.balance_to_date + 2.5
				else:
					slip.balance_on_pay_slip = slip.balance_to_date
		return res
	
	def compute_days_taken_in_the_month(self):
		for paye in self:
			paye.days_taken_in_the_month = sum(
				paye.worked_days_line_ids.filtered(lambda w: w.work_entry_type_id.code == 'LEAVE100').mapped(
					'number_of_days'))
	
	@api.onchange('previous_paid_leave_balance')
	def onchange_previous_paid_leave_balance(self):
		for paye in self:
			paye.new_balance_in_the_month = (paye.previous_paid_leave_balance + float(
				paye.gain_on_current_month)) - paye.days_taken_in_the_month
	
	def _compute_new_balance_in_the_month(self):
		for paye in self:
			paye.new_balance_in_the_month = (paye.previous_paid_leave_balance + float(
				paye.gain_on_current_month)) - paye.days_taken_in_the_month
	
	def calculate_cumul_leaves(self, date):
		holiday_status_id = self.env.ref('hr_holidays.holiday_status_cl')
		leaves = self.env['hr.leave'].search([('employee_id', '=', self.employee_id.id), ('state', '=', 'validate'),
		                                      ('holiday_status_id', '=', holiday_status_id.id),
		                                      ('request_date_from', '<', date),
		                                      ('request_date_to', '<=', date)])
		return sum(leaves.mapped('number_of_days'))
	
	def calculate_cumul_allocation(self, date):
		holiday_status_id = self.env['hr.leave.type'].search(
			[('is_paid_time_off', '=', True), ('company_id', '=', self.employee_id.company_id.id)])
		allocation_regulars = self.env['hr.leave.allocation'].search(
			[('state', '=', 'validate'), ('allocation_type', '=', 'regular'),
			 ('holiday_status_id', '=', holiday_status_id.id)
				, ('employee_id', '=', self.employee_id.id),
             ('date_from', '<=', date), '|', ('date_to', '>=', date), ('date_to', '=', False)])
		allocation_accruals = self.env['hr.leave.allocation'].search(
			[('state', '=', 'validate'), ('allocation_type', '=', 'accrual'),
			 ('holiday_status_id', '=', holiday_status_id.id),
			 ('employee_id', '=', self.employee_id.id),
			 ('date_from', '<=', date), '|', ('date_to', '>=', date), ('date_to', '=', False)])
		level_value = 0.00
		today = fields.Date.today()
		for allocation_accrual in allocation_accruals:
			date_from = self.date_from - timedelta(days=1)
			level_ids = allocation_accrual.accrual_plan_id.level_ids.sorted('sequence')
			if not level_ids:
				continue
			first_level = level_ids[0]
			first_level_start_date = allocation_accrual.date_from + get_timedelta(first_level.start_count,
			                                                                      first_level.start_type)
			if today < first_level_start_date:
				continue
			lastcall = first_level_start_date
			nextcall = first_level._get_next_date(lastcall)
			if len(level_ids) > 1:
				second_level_start_date = allocation_accrual.date_from + get_timedelta(level_ids[1].start_count,
				                                                                       level_ids[1].start_type)
				nextcall = min(second_level_start_date, nextcall)
			days_added_per_level = defaultdict(lambda: 0)
			while nextcall <= date_from:
				(current_level, current_level_idx) = allocation_accrual._get_current_accrual_plan_level_id(nextcall)
				current_level_maximum_leave = current_level.maximum_leave if current_level.added_value_type == "days" else current_level.maximum_leave / (
						allocation_accrual.employee_id.sudo().resource_id.calendar_id.hours_per_day or HOURS_PER_DAY)
				new_nextcall = current_level._get_next_date(nextcall)
				period_start = current_level._get_previous_date(lastcall)
				period_end = current_level._get_next_date(lastcall)
				if current_level_idx < (
						len(level_ids) - 1) and allocation_accrual.accrual_plan_id.transition_mode == 'immediately':
					next_level = level_ids[current_level_idx + 1]
					current_level_last_date = allocation_accrual.date_from + get_timedelta(next_level.start_count,
					                                                                       next_level.start_type)
					if nextcall != current_level_last_date:
						new_nextcall = min(new_nextcall, current_level_last_date)
				days_added_per_level[current_level] += allocation_accrual._process_accrual_plan_level(
					current_level, period_start, lastcall, period_end, nextcall)
				if current_level_maximum_leave > 0 and sum(
						days_added_per_level.values()) > current_level_maximum_leave:
					days_added_per_level[current_level] -= sum(
						days_added_per_level.values()) - current_level_maximum_leave
				lastcall = nextcall
				nextcall = new_nextcall
			if days_added_per_level:
				number_of_days_to_add = sum(days_added_per_level.values())
				max_allocation_days = current_level_maximum_leave + (
					allocation_accrual.leaves_taken if allocation_accrual.type_request_unit != "hour" else allocation_accrual.leaves_taken / (
							allocation_accrual.employee_id.sudo().resource_id.calendar_id.hours_per_day or HOURS_PER_DAY))
				level_value += min(number_of_days_to_add,
				                   max_allocation_days) if current_level_maximum_leave > 0 else number_of_days_to_add
		return level_value + sum(allocation_regulars.mapped('number_of_days'))
	
	@api.depends('employee_id', 'date_from')
	def compute_previous_paid_leave_balance(self):
		for payslip in self:
			payslip.previous_paid_leave_balance = 0.00
			if payslip.employee_id:
				payslip.previous_paid_leave_balance = payslip.calculate_cumul_allocation(
					payslip.date_from) - payslip.calculate_cumul_leaves(payslip.date_from)
	
	def refresh_payslip_leave_situation(self):
		self.compute_days_taken_in_the_month()
		self._compute_new_balance_in_the_month()
		self.compute_previous_paid_leave_balance()
	
	# def _get_remaining_leaves(self):
	#     for paye in self:
	#         paye.balance_to_date = paye.employee_id.leaves_count
	
	# def _get_balance_remaining_leaves(self):
	#     for paye in self:
	#         if paye.gain_on_current_month == "2":
	#             paye.balance_on_pay_slip = paye.balance_to_date + 2.5
	#         elif paye.gain_on_current_month == "0":
	#             paye.balance_on_pay_slip = paye.balance_to_date
	
	@api.onchange('employee_id')
	def get_balance_to_date(self):
		for paye in self:
			paye.balance_to_date = paye.employee_id.leaves_count
			if paye.gain_on_current_month == "2.5":
				paye.balance_on_pay_slip = paye.balance_to_date + 2.5
			elif paye.gain_on_current_month == "0":
				paye.balance_on_pay_slip = paye.balance_to_date
	
	@api.onchange('gain_on_current_month', 'employee_id')
	def change_gain_on_current_month(self):
		for paye in self:
			if paye.gain_on_current_month == "2.5":
				paye.balance_on_pay_slip = paye.balance_to_date + 2.5
			elif paye.gain_on_current_month == "0":
				paye.balance_on_pay_slip = paye.balance_to_date


class HRPayslipPaymentMode(models.Model):
	_name = "hr.payslip.payment.mode"
	_description = "HR Payslip Payment Mode"
	
	name = fields.Char(required=True)
