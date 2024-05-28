# -*- coding: utf-8 -*-

from odoo import models, fields, _, SUPERUSER_ID
from odoo.exceptions import UserError
from odoo.tools import float_compare


class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    is_return = fields.Boolean(default=False)

    def set_sp_return(self):
        self.is_return = True

    def button_validate(self):
        result = super().button_validate()

        res = True
        if self.env.company.rule_type == 'sale_purchase' and self.is_return and self.sale_id and not self.sale_id.auto_generated:
            move_ids = self.move_ids
            if any(float_compare(move_line.quantity, move_line.quantity, precision_rounding=move_line.product_uom.rounding) != 0 for move_line in move_ids):
                raise UserError(_("Can't validate return. Please click on 'Copy quantity' button first and try again."))

            # TODO: Manage this return process for:
            #  - multiple stock.picking (po_picking_id) linked to purchase.order
            #  - multiple stock.picking (so_picking_id) linked to sale.order in related company
            purchase_id = self.env['purchase.order'].search(
                [('origin', 'like', self.sale_id.name)], order='id DESC', limit=1)
            po_picking_id = purchase_id.picking_ids.filtered(lambda x: x.state == 'done' and not x.is_return)
            if po_picking_id:
                po_sp_return_id = po_picking_id.create_po_sp_return(move_ids)
                po_sp_return_id.validate_picking()

                company_id = self.env['res.company'].search([('partner_id', '=', purchase_id.partner_id.id)])
                sale_id = self.env['sale.order'].with_user(SUPERUSER_ID).with_company(company_id).search([
                    ('auto_generated', '=', True),
                    ('auto_purchase_order_id', '=', purchase_id.id),
                ])
                so_picking_id = sale_id.picking_ids.filtered(lambda x: x.state == 'done' and not x.is_return)
                so_sp_return_id = so_picking_id.create_so_sp_return_in_related_company(move_ids, company_id)
                so_sp_return_id.validate_picking()

                res = res and po_sp_return_id and so_sp_return_id

        return res and result

    def create_po_sp_return(self, move_ids):
        return_picking_id = self.env['stock.return.picking'].create({
            'picking_id': self.id
        })
        return_picking_id.set_return_values(move_ids, self)
        new_picking_id, pick_type_id = return_picking_id._create_returns()
        return self.browse(new_picking_id)

    def create_so_sp_return_in_related_company(self, move_ids, company_id):
        return_picking_id = self.env['stock.return.picking'].create({
            'picking_id': self.id
        })
        return_picking_id.set_return_values(move_ids, self)

        current_company_id = self.env.company
        user = current_company_id.intercompany_user_id and current_company_id.intercompany_user_id.id or SUPERUSER_ID
        new_picking_id, pick_type_id = return_picking_id.with_user(user).with_company(company_id)._create_returns()
        return self.browse(new_picking_id)

    def validate_picking(self):
        if self.state == 'waiting':
            # Set done quantity manually
            for move_line in self.move_ids:
                move_line._set_quantity_done(move_line.quantity)
        else:
            self.action_confirm()
            if self.state != 'assigned':
                self.action_assign()
                if self.state != 'assigned':
                    raise UserError(_("Document: %s.\nCould not reserve all requested products.") % self.name)
            self.move_ids._set_quantities_to_reservation()

        self.button_validate()
