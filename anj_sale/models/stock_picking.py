# -*- coding: utf-8 -*-

from odoo import models, fields
import calendar
mois_fr = {
    1: "janvier",
    2: "février",
    3: "mars",
    4: "avril",
    5: "mai",
    6: "juin",
    7: "juillet",
    8: "août",
    9: "septembre",
    10: "octobre",
    11: "novembre",
    12: "décembre"
}
class StockPicking(models.Model):
    _inherit = 'stock.picking'

    note_client = fields.Char(string="Note", related="sale_id.note_client", store=True)

    scheduled_date_month_year = fields.Char(compute='_get_month_yars')

    def _get_month_yars(self):
        for rec in self:
            rec.scheduled_date_month_year = mois_fr[rec.scheduled_date.month] + ' ' + str(rec.scheduled_date.year)