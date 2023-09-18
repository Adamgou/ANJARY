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

    # def button_mark_done(self):
    #     self._button_mark_done_sanity_checks()
    #
    #     if not self.env.context.get('button_mark_done_production_ids'):
    #         self = self.with_context(button_mark_done_production_ids=self.ids)
    #     res = self._pre_button_mark_done()
    #     if res is not True:
    #         return res
    #
    #     if self.env.context.get('mo_ids_to_backorder'):
    #         productions_to_backorder = self.browse(self.env.context['mo_ids_to_backorder'])
    #         productions_not_to_backorder = self - productions_to_backorder
    #         close_mo = False
    #     else:
    #         productions_not_to_backorder = self
    #         productions_to_backorder = self.env['mrp.production']
    #         close_mo = True
    #
    #     self.workorder_ids.button_finish()
    #
    #     backorders = productions_to_backorder._generate_backorder_productions(close_mo=close_mo)
    #     productions_not_to_backorder._post_inventory(cancel_backorder=True)
    #     productions_to_backorder._post_inventory(cancel_backorder=True)
    #
    #     # if completed products make other confirmed/partially_available moves available, assign them
    #     done_move_finished_ids = (productions_to_backorder.move_finished_ids | productions_not_to_backorder.move_finished_ids).filtered(lambda m: m.state == 'done')
    #     done_move_finished_ids._trigger_assign()
    #
    #     # Moves without quantity done are not posted => set them as done instead of canceling. In
    #     # case the user edits the MO later on and sets some consumed quantity on those, we do not
    #     # want the move lines to be canceled.
    #     (productions_not_to_backorder.move_raw_ids | productions_not_to_backorder.move_finished_ids).filtered(lambda x: x.state not in ('done', 'cancel')).write({
    #         'state': 'done',
    #         'product_uom_qty': 0.0,
    #     })
    #
    #     for production in self:
    #         production.write({
    #             'date_finished': fields.Datetime.now(),
    #             'product_qty': production.qty_produced,
    #             'priority': '0',
    #             'is_locked': True,
    #             'state': 'done',
    #         })
    #
    #     for workorder in self.workorder_ids.filtered(lambda w: w.state not in ('done', 'cancel')):
    #         workorder.duration_expected = workorder._get_duration_expected()
    #
    #     if not backorders:
    #         if self.env.context.get('from_workorder'):
    #             return {
    #                 'type': 'ir.actions.act_window',
    #                 'res_model': 'mrp.production',
    #                 'views': [[self.env.ref('mrp.mrp_production_form_view').id, 'form']],
    #                 'res_id': self.id,
    #                 'target': 'main',
    #             }
    #         return True
    #     context = self.env.context.copy()
    #     context = {k: v for k, v in context.items() if not k.startswith('default_')}
    #     for k, v in context.items():
    #         if k.startswith('skip_'):
    #             context[k] = False
    #     action = {
    #         'res_model': 'mrp.production',
    #         'type': 'ir.actions.act_window',
    #         'context': dict(context, mo_ids_to_backorder=None, button_mark_done_production_ids=None)
    #     }
    #     if len(backorders) == 1:
    #         action.update({
    #             'view_mode': 'form',
    #             'res_id': backorders[0].id,
    #         })
    #     else:
    #         action.update({
    #             'name': _("Backorder MO"),
    #             'domain': [('id', 'in', backorders.ids)],
    #             'view_mode': 'tree,form',
    #         })
    #         # filtered(lambda bank: bank.company_id is False or bank.company_id == self.company_id)
    #     bom_lin_ids = self.bom_id.bom_line_ids
    #     for b_l_ids in bom_lin_ids:
    #         if self.move_raw_ids.filtered(lambda r: r.product_id.id == b_l_ids.product_id.id):
    #             for stock_m in self.move_raw_ids:
    #                 b_l_ids.product_qty = stock_m.filtered(lambda r: r.product_id.id == b_l_ids.product_id.id).quantity_done/self.product_qty
    #     return action

    # def button_mark_done(self):
    #     res = super().button_mark_done()
    #
    #     sum_qt_pr = 0
    #     pid = 0
    #     booml_dict = {}
    #     for mv_row in self.move_raw_ids:
    #         if pid == mv_row.product_id.id:
    #             sum_qt_pr += mv_row.quantity_done
    #         else:
    #             sum_qt_pr = mv_row.quantity_done
    #         if mv_row.bom_line_id:
    #             booml_dict[mv_row.bom_line_id] = sum_qt_pr
    #         pid = mv_row.product_id.id
    #
    #
    #     for bl_ids in self.move_raw_ids.filtered(lambda m: m.bom_line_id):
    #         if bl_ids:
    #             if self.qty_producing != 0:
    #                 self.env['mrp.bom.line'].browse(bl_ids.bom_line_id.id).write({'product_qty': bl_ids.quantity_done/self.qty_producing})
    #
    #                 booml_dict
    #             else:
    #                 self.env['mrp.bom.line'].browse(bl_ids.bom_line_id.id).write({'product_qty': 0.00})
    #
    #     return res


    def button_mark_done(self):
        res = super().button_mark_done()

        quantites_par_article = {}

        for ligne in self.move_raw_ids:
            article = ligne.product_id.id
            quantite = ligne.quantity_done

            if article in quantites_par_article:
                quantites_par_article[article] += quantite
            else:
                quantites_par_article[article] = quantite

        for products, qty in quantites_par_article.items():
            for bl_ids in self.move_raw_ids.filtered(lambda m: m.bom_line_id):
                if bl_ids:
                    if self.qty_producing != 0:
                        self.env['mrp.bom.line'].search([('id', '=', bl_ids.bom_line_id.id), ('product_id', '=', products)]).write({'product_qty': qty/self.qty_producing})
                        # self.env['mrp.bom.line'].browse(bl_ids.bom_line_id.id).write({'product_qty': bl_ids.quantity_done/self.qty_producing})
                    else:
                        self.env['mrp.bom.line'].search([('id', '=', bl_ids.bom_line_id.id), ('product_id', '=', products)]).write({'product_qty': 0.00})

        return res