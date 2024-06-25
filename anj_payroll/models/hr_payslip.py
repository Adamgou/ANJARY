# coding: utf-8

from odoo import models, fields


class HRPayslip(models.Model):
    _inherit = "hr.payslip"

    payment_mode_id = fields.Many2one(comodel_name="hr.payslip.payment.mode")


class HRPayslipPaymentMode(models.Model):
    _name = "hr.payslip.payment.mode"
    _description = "HR Payslip Payment Mode"

    name = fields.Char(required=True)
