# -*- coding: utf-8 -*-
from odoo.exceptions import UserError, Warning

from odoo import models, fields, api

class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    def start_subscription(self):
        res = super(SaleSubscription, self).start_subscription()
        line_busy = self.env['sale.subscription.line'].search([('analytic_account_id.stage_id', '=', self.env.ref('sale_subscription.sale_subscription_stage_in_progress').id), ('analytic_account_id', '!=', self.id)])

        if line_busy:
            raise UserError(f"L'immobilier {','.join(line_busy.mapped('name'))} est en cours d abonnement")

        return res