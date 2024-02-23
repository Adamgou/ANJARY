# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError, Warning

class HrSalaryAttachment(models.Model):
    _inherit = "hr.salary.attachment"

    deduction_type = fields.Selection(
        selection=[
            ('attachment', 'Attachment of Salary'),
            ('assignment', 'Assignment of Salary'),
            ('child_support', 'Child Support'),
            ('special_advance', 'Special Advance'),
            ('advance_15th', 'Advance 15th'),
        ],
        string='Type',
        required=True,
        default='attachment',
        tracking=True,
    )
    #deduction_type = fields.Selection(selection_add=[('special_advance', 'Special Advance'),('advance_15th', 'Advance 15th')], ondelete={'special_advance': 'cascade', 'advance_15th': 'cascade'})

    @api.onchange('total_amount')
    def _onchange_total_amount(self):
        if self.deduction_type == 'advance_15th':
            if self.total_amount > self.employee_id.contract_id.wage:
                raise UserError(_("The total amount must be less than the wage of the employee."))
            elif self.total_amount > self.employee_id.contract_id.wage * 0.5:
                return {
                    'warning': {
                        'title': _('Warning'),
                        'message': _('The total amount is more than 50% of the wage of the employee.')
                    }
                }

