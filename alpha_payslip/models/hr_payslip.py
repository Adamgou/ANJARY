# -*- coding: utf-8 -*-
from datetime import date

from odoo import fields, models, api
# from odoo.exceptions import UserError, Warning
# raise UserError(f"La date d'entrée ")



class Hr_Payslip(models.Model):
    _inherit = 'hr.payslip'

    def get_age(self, birth_date,date_bis):
        if birth_date:
            today = date.today()

            if date_bis:
                end_date=date_bis
                age = end_date.year - birth_date.year 
                

            else:
                age = today.year - birth_date.year 
        age+=1
        return age

    def get_spent_monthly_hours(self,monthly_hours):
        if monthly_hours:
            spent_hours=round(((52*monthly_hours)/12),2)
            return spent_hours