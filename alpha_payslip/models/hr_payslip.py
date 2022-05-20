# -*- coding: utf-8 -*-
from datetime import date

from odoo import fields, models, api


class Hr_Payslip(models.Model):
    _inherit = 'hr.payslip'

    def get_age(self, birth_date):
        if birth_date:
            today = date.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

            return age
