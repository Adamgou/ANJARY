# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, SUPERUSER_ID


class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    is_return = fields.Boolean(default=False)

    def set_sp_return(self):
        self.is_return = True

    def button_validate(self):
        result = super(StockPickingInherit, self).button_validate()

        res = True
        if self.env.company.rule_type == 'sale_purchase' and self.is_return and self.sale_id and not self.sale_id.auto_generated:
            move_lines = self.move_lines

            # TODO: Manage this return process for:
            #  - multiple purchase.order (purchase_id) linked to sale.order
            #  - multiple stock.picking (po_picking_id) linked to purchase.order
            #  - multiple stock.picking (so_picking_id) linked to sale.order in related company
            purchase_id = self.sale_id._get_purchase_orders()
            po_picking_id = purchase_id.picking_ids.filtered(lambda x: x.state == 'done' and not x.is_return)
            po_sp_return_id = po_picking_id.create_po_sp_return(move_lines)
            po_sp_return_id.validate_picking()

            company_id = self.env['res.company'].search([('partner_id', '=', purchase_id.partner_id.id)])
            sale_id = self.env['sale.order'].with_user(SUPERUSER_ID).with_company(company_id).search([
                ('auto_generated', '=', True),
                ('auto_purchase_order_id', '=', purchase_id.id),
            ])
            so_picking_id = sale_id.picking_ids.filtered(lambda x: x.state == 'done' and not x.is_return)
            so_sp_return_id = so_picking_id.create_so_sp_return_in_related_company(move_lines, company_id)
            so_sp_return_id.validate_picking()

            res = res and po_sp_return_id and so_sp_return_id

        return res and result

    def create_po_sp_return(self, move_lines):
        return_picking_id = self.env['stock.return.picking'].create({
            'picking_id': self.id
        })
        return_picking_id.set_return_values(move_lines, self)
        new_picking_id, pick_type_id = return_picking_id._create_returns()
        return self.browse(new_picking_id)

    def create_so_sp_return_in_related_company(self, move_lines, company_id):
        return_picking_id = self.env['stock.return.picking'].create({
            'picking_id': self.id
        })
        return_picking_id.set_return_values(move_lines, self)

        current_company_id = self.env.company
        user = current_company_id.intercompany_user_id and current_company_id.intercompany_user_id.id or SUPERUSER_ID
        new_picking_id, pick_type_id = return_picking_id.with_user(user).with_company(company_id)._create_returns()
        return self.browse(new_picking_id)

    def validate_picking(self):
        self.action_set_quantities_to_reservation()
        self.button_validate()
