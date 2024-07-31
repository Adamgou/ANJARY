# -*- coding: utf-8 -*-

from odoo import models, fields


class HrLeaveType(models.Model):
	_inherit = "hr.leave.type"
	
	is_paid_time_off = fields.Boolean(string="Is paid time off")
