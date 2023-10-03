# -*- coding: utf-8 -*-


import json
import datetime
import math
import re
import warnings

from collections import defaultdict
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_round, float_is_zero, format_datetime
from odoo.tools.misc import OrderedSet, format_date, groupby as tools_groupby

from odoo.addons.stock.models.stock_move import PROCUREMENT_PRIORITIES


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def button_mark_done(self):
        res = super().button_mark_done()
        MrpBomLine = self.env['mrp.bom.line']
        number_of_mo = float(self.env['ir.config_parameter'].sudo().get_param(
            'anj_production.number_of_mo'))
        last_records = self.search([('bom_id', '=', self.bom_id.id)], order='create_date desc', limit=number_of_mo)
        quantites_par_article = {}
        qty_producing = 0
        bom_qty_to_produced = self.bom_id.product_qty
        for mrp_production_record in last_records:
            for move_l in mrp_production_record.move_raw_ids:
                if not move_l.bom_line_id and move_l.product_id not in self.move_raw_ids.filtered(
                        lambda m: m.bom_line_id).product_id:
                    new_line = MrpBomLine.create({
                        'bom_id': self.bom_id.id,
                        'product_id': move_l.product_id.id,
                        'product_qty': move_l.forecast_availability,
                        'product_uom_id': move_l.product_uom.id
                    })
                    move_l.bom_line_id = new_line.id
                    move_l.bom_line_id.product_id = new_line.product_id

            for mrp_bom_line in self.env['mrp.bom.line'].search([('bom_id', '=', self.bom_id.id)]):
                if mrp_bom_line not in mrp_production_record.move_raw_ids.filtered(lambda m: m.bom_line_id).bom_line_id:
                    mrp_bom_line.unlink()

            for ligne in mrp_production_record.move_raw_ids:
                article = ligne.product_id.id
                quantite = ligne.quantity_done

                if article in quantites_par_article:
                    quantites_par_article[article] += quantite
                else:
                    quantites_par_article[article] = quantite
            qty_producing += mrp_production_record.qty_producing

        for products, qty in quantites_par_article.items():
            for bl_ids in self.move_raw_ids.filtered(lambda m: m.bom_line_id):
                if bl_ids:
                    if qty_producing != 0:
                        self.env['mrp.bom.line'].search(
                            [('id', '=', bl_ids.bom_line_id.id), ('product_id', '=', products)]).write(
                            {'product_qty': (qty * bom_qty_to_produced) / qty_producing})
                    else:
                        self.env['mrp.bom.line'].search(
                            [('id', '=', bl_ids.bom_line_id.id), ('product_id', '=', products)]).write(
                            {'product_qty': 0.00})
        return res
