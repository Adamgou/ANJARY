# coding: utf-8

from odoo import models, fields


class StockPicking(models.Model):
    _inherit = "stock.picking"

    note_client = fields.Char(string="Note", related="sale_id.note_client", store=True)
