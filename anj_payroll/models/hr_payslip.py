# coding: utf-8

from collections import defaultdict
from datetime import timedelta

from odoo import models, fields, api
from odoo.addons.resource.models.utils import HOURS_PER_DAY
from odoo.tools.date_utils import get_timedelta


class HRPayslip(models.Model):
	_inherit = "hr.payslip"
	
	payment_mode_id = fields.Many2one(comodel_name="hr.payslip.payment.mode")
	

class HRPayslipPaymentMode(models.Model):
	_name = "hr.payslip.payment.mode"
	_description = "HR Payslip Payment Mode"
	
	name = fields.Char(required=True)
