# -*- coding: utf-8 -*-

from odoo import models, _, Command
from odoo.exceptions import UserError


class ReturnPickingInherit(models.TransientModel):
    _inherit = 'stock.return.picking'

    def _create_returns(self):
        id_new_picking, picking_type_id = super()._create_returns()

        new_picking_id = self.env['stock.picking'].browse(id_new_picking)
        new_picking_id.set_sp_return()
        
        return id_new_picking, picking_type_id

    def set_return_values(self, move_ids, related_picking_id):
        move_dest_exists = False
        product_return_moves = [Command.clear()]

        if self.picking_id and self.picking_id.state != 'done':
            raise UserError(_("You may only return Done pickings."))

        # In case we want to set specific default values (e.g. 'to_refund'), we must fetch the
        # default values for creation.
        line_fields = [f for f in self.env['stock.return.picking.line']._fields.keys()]
        product_return_moves_data_tmpl = self.env['stock.return.picking.line'].default_get(line_fields)

        move_ids = related_picking_id.move_ids.filtered(
            lambda x: x.product_id.id in move_ids.mapped('product_id').ids)
        for move in move_ids:
            if move.state == 'cancel':
                continue
            if move.scrapped:
                continue
            if move.move_dest_ids:
                move_dest_exists = True
            product_return_moves_data = dict(product_return_moves_data_tmpl)
            product_return_moves_data.update(self._prepare_stock_return_picking_line_vals_from_move(move))

            move_id = self.env['stock.move'].search([
                ('id', 'in', move_ids.ids),
                ('product_id', '=', move.product_id.id)
            ])
            product_return_moves_data['quantity'] = move_id.product_uom_qty

            product_return_moves.append(Command.create(product_return_moves_data))

        if self.picking_id and not product_return_moves:
            raise UserError(_("No products to return (only lines in Done state and not fully returned yet can be returned)."))

        self.product_return_moves = product_return_moves
        self.move_dest_exists = move_dest_exists
        self.parent_location_id = self.picking_id.picking_type_id.warehouse_id and self.picking_id.picking_type_id.warehouse_id.view_location_id.id or self.picking_id.location_id.location_id.id
        self.original_location_id = self.picking_id.location_id.id
        location_id = self.picking_id.location_id.id

        if self.picking_id.picking_type_id.return_picking_type_id.default_location_dest_id.return_location:
            location_id = self.picking_id.picking_type_id.return_picking_type_id.default_location_dest_id.id

        self.location_id = location_id
