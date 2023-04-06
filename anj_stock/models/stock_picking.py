# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from datetime import datetime, timedelta


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    picking_date_due = fields.Datetime(string="Date due", compute="_compute_date_due")

    def _compute_date_due(self):
        for picking in self:
            # scheduled_date = datetime.strptime(picking.scheduled_date, '%Y-%m-%d %H:%M:%S')
            nbr_days = picking.sale_id.payment_term_id.line_ids.days
            picking.picking_date_due = picking.scheduled_date + timedelta(days=nbr_days)
