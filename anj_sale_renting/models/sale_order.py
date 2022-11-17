# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    car_registration_ids = fields.Many2many(compute='_compute_car_registration_ids', store=True)

    @api.depends('order_line.selected_lot_ids')
    def _compute_car_registration_ids(self):
        for rec in self:
            rec.car_registration_ids = [(6, 0, rec.order_line.mapped('selected_lot_ids').mapped('id'))]

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    selected_lot_ids = fields.Many2many('stock.production.lot', 'rental_selected_lot_rel', domain="[('product_id','=',product_id)]", copy=False)