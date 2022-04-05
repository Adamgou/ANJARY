# -*- coding: utf-8 -*-
from odoo.exceptions import UserError, Warning

from odoo import models, fields, api

class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    def start_subscription(self):
        
        res = super(SaleSubscription, self).start_subscription()
        for line in self.recurring_invoice_line_ids:
            if line.product_id.is_insubscription ==False:
                line.product_id.write({"is_insubscription": True})
            else:
                raise UserError(f"Votre article {line.product_id.name} ayant comme reférence interne {line.product_id.default_code} est en cours d abonnement")

            
        return res