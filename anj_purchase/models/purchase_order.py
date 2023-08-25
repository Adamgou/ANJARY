# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    def inter_company_create_sale_order(self, company):
        intercompany_uid = company.intercompany_user_id and company.intercompany_user_id.id or False
        if not intercompany_uid:
            raise UserError(_(
                'Provide at least one user for inter company relation for %(name)s',
                name=company.name,
            ))
        # check intercompany user access rights
        if not self.env['sale.order'].check_access_rights('create', raise_exception=False):
            raise UserError(_(
                "Inter company user of company %(name)s doesn't have enough access rights",
                name=company.name,
            ))

        for rec in self:
            # check pricelist currency should be same with SO/PO document
            company_partner = rec.company_id.partner_id.with_user(intercompany_uid)
            if rec.currency_id.id != company_partner.property_product_pricelist.currency_id.id:
                raise UserError(_(
                    'You cannot create SO from PO because sale price list currency is different '
                    'than purchase price list currency.\n'
                    'The currency of the SO is obtained from the pricelist of the company partner.\n\n'
                    '(SO currency: %(so_currency)s, Pricelist: %(pricelist)s, Partner: %(partner)s (ID: %(id)s))',
                    so_currency=rec.currency_id.name,
                    pricelist=company_partner.property_product_pricelist.display_name,
                    partner=company_partner.display_name,
                    id=company_partner.id,
                ))

            # create the SO and generate its lines from the PO lines
            # read it as sudo, because inter-compagny user can not have the access right on PO
            direct_delivery_address = rec.picking_type_id.warehouse_id.partner_id.id or rec.dest_address_id.id
            sale_order_data = rec.sudo()._prepare_sale_order_data(
                rec.name, company_partner, company,
                direct_delivery_address or False)
            inter_user = self.env['res.users'].sudo().browse(intercompany_uid)
            # lines are browse as sudo to access all data required to be copied on SO line (mainly for company dependent field like taxes)
            for line in rec.order_line.sudo():
                sale_order_data['order_line'] += [(0, 0, rec._prepare_sale_order_line_data(line, company))]
            sale_order = self.env['sale.order'].with_context(allowed_company_ids=inter_user.company_ids.ids).with_user(intercompany_uid).create(sale_order_data)
            sale_order.order_line._compute_tax_id()
            msg = _("Automatically generated from %(origin)s of company %(company)s.", origin=self.name, company=rec.company_id.name)
            sale_order.message_post(body=msg)

            # write vendor reference field on PO
            if not rec.partner_ref:
                rec.partner_ref = sale_order.name

            #Validation of sales order
            if company.auto_validation:
                sale_order.with_user(intercompany_uid).action_confirm()
                if sale_order.picking_ids:
                    for sale_pickings in sale_order.picking_ids:
                        sale_pickings.button_validate()
        # self._get_sale_order_inter_company(sale_order=sale_order)


    # def _get_sale_order_inter_company(self, sale_order):
    #     return sale_order

    def button_confirm(self):
        for order in self:
            if order.state not in ['draft', 'sent']:
                continue
            order._add_supplier_to_product()
            # Deal with double validation process
            if order._approval_allowed():
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
            if order.partner_id not in order.message_partner_ids:
                order.message_subscribe([order.partner_id.id])
            if order.picking_ids:
                for order_picking in order.picking_ids:
                    order_picking.button_validate()
        # self.env['stock.picking'].browse(self.picking_ids.id).button_validate()

        return True