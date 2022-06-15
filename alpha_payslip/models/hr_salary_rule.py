from odoo import fields, models, _, api
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class ModelName(models.Model):
    _inherit = 'hr.salary.rule'
    alpha_hour_python_compute = fields.Text(string='Python Code')

    def _compute_alpha_hour(self):
        try:
            return float(safe_eval(self.alpha_hour_python_compute))
        except Exception as e:
            raise UserError(_('Wrong python_code for alpha_hour %s (%s).\nError: %s') % (self.name, self.code, e))

    alpha_base_salary_python_compute = fields.Text(string='Python Code')

    def _compute_alpha_base_salary(self):
        try:
            return float(safe_eval(self.alpha_base_salary_python_compute))
        except Exception as e:
            raise UserError(_('Wrong python_code for alpha_base_salary %s (%s).\nError: %s') % (self.name, self.code, e))
