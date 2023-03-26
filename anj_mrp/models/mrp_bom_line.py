from odoo import fields, models, api


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'
    product_qty = fields.Float(digits='Payroll Rate')
