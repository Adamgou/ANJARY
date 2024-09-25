# coding: utf-8

from odoo import models


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"


    def get_paperformat(self):
        if self.env.company.name.lower().startswith('jara') and self.model == 'account.move':
            return  self.env.ref('anj_account.paperformat_account_a4')
        elif not self.env.company.name.lower().startswith('jara') and self.model == 'account.move':
            return self.env.ref('base.paperformat_euro')
        else:
            return super(IrActionsReport, self).get_paperformat()
        
