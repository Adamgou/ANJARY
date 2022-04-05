# -*- coding: utf-8 -*-
from odoo.exceptions import UserError, Warning

from odoo import models, fields, api

class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    def start_subscription(self):
        
        res = super(SaleSubscription, self).start_subscription()
        for line in self.recurring_invoice_line_ids:
            ref_intern=line.product_id.default_code or " "
            if line.product_id.is_insubscription ==False:
                line.product_id.write({"is_insubscription": True})
            else:
                raise UserError(f"L'immobilier {line.product_id.name} {ref_intern} est en cours d abonnement")

            
        return res

    def set_close(self):
        res = super(SaleSubscription, self).set_close()
        for line in self.recurring_invoice_line_ids:
            if line.product_id.is_insubscription ==True:
                line.product_id.write({"is_insubscription": False})
            

                
        return res