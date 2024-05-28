# coding: utf-8

from datetime import timedelta

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    picking_date_due = fields.Datetime(string="Date due", compute="_compute_date_due")

    def _compute_date_due(self):
        for picking in self:
            nbr_days = picking.sale_id.payment_term_id.line_ids.nb_days
            picking.picking_date_due = picking.scheduled_date + timedelta(days=nbr_days)
