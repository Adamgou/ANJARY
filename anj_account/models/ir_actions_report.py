# coding: utf-8

from odoo import models


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    def get_paperformat(self):
        """
            Get paperformat according to company
        :return:
        """
        if (
            self.env.company.name.lower().startswith("jara")
            and self.model == "account.move"
        ):
            return self.env.ref("anj_account.paperformat_account_a4")
        if (
            self.env.company.name.lower().startswith("biskot")
            and self.model == "account.move"
        ):
            return self.env.ref("anj_account.paperformat_account_biskot_a4")
        if (
            not self.env.company.name.lower().startswith("jara")
            and self.model == "account.move"
        ):
            return self.env.ref("base.paperformat_euro")
        return super().get_paperformat()
