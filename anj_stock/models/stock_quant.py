from odoo import fields, models, _, api
from odoo.exceptions import UserError


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    is_applying_quant = fields.Boolean(compute='_compute_is_applying_quant')



    def _compute_is_applying_quant(self):
        if self.env.user.has_group('anj_stock.anj_is_applying_quant_stock'):
            self.is_applying_quant = True
        else:
            self.is_applying_quant = False