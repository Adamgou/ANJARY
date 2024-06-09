# coding: utf-8

from odoo import fields, models


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    product_qty = fields.Float(digits="Payroll Rate")
