# coding: utf-8


from odoo.osv.expression import OR, AND
from odoo import api, fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    related_biskot = fields.Boolean(related='company_id.is_biskot')
    pdv_tsaralalana = fields.Boolean(string='Pdv tsaralalana')
    pdv_ivato = fields.Boolean(string='Pdv ivato')

    def _get_available_product_domain(self):
        res = super(PosConfig,self)._get_available_product_domain()
        if self.pdv_tsaralalana:
            res += [ ('available_in_pdv_tsaralalana','=',True),]
        elif self.pdv_ivato:
            res += [('available_in_pdv_ivato','=',True),]
        return res