# -*- coding: utf-8 -*-


import itertools
import logging
from collections import defaultdict

from odoo import api, fields, models, tools, _, SUPERUSER_ID
from odoo.exceptions import ValidationError, RedirectWarning, UserError
from odoo.osv import expression

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # def _get_default_values_vendor(self):
    #     default_values = []
    #     if self.env.company.partner_id.default_product_supplier:
    #         default_values = [(0, 0, {
    #             'name': self.env['res.partner'].search([('id', '=', self.env.company.partner_id.default_product_supplier.id)], limit=1),
    #         })]
    #     return default_values
    #
    # seller_ids = fields.One2many('product.supplierinfo', 'product_tmpl_id', 'Vendors', depends_context=('company',), help="Define vendor pricelists.", default=lambda self: self._get_default_values_vendor())

    # @api.onchange('list_price')
    # def _change_seller_ids_price(self):
    #     if self.env.company.partner_id.default_product_supplier:
    #         self.seller_ids.price = (self.list_price * self.env.company.partner_id.pourcent_price_product)/100





    # @api.onchange('company_ids')
    # def _change_seller_ids_price(self):
    #     if self.company_ids.filtered(lambda c: c.partner_id.default_product_supplier):
    #         self.seller_ids.price = (self.list_price * self.env.company.partner_id.pourcent_price_product)/100

    @api.model_create_multi
    def create(self, vals_list):
        templates = super(ProductTemplate, self).create(vals_list)
        for templates in templates:
            if templates.company_ids.filtered(lambda c: c.partner_id.default_product_supplier):
            
                self.env['product.supplierinfo'].sudo().create({
                    'product_tmpl_id': templates.id,
                    'name': templates.company_ids.filtered(lambda c: c.partner_id.default_product_supplier).partner_id.default_product_supplier.id,
                    'price': templates.list_price * templates.company_ids.filtered(lambda c: c.partner_id.default_product_supplier).partner_id.pourcent_price_product,
                    'company_id': templates.company_ids.filtered(lambda c: c.partner_id.default_product_supplier).id
                })

        return templates


    def write(self, vals):
        templates = super(ProductTemplate, self).write(vals)

        for templates in self:
            if templates.company_ids.filtered(lambda c: c.partner_id.default_product_supplier):
                if self.env['product.supplierinfo'].sudo().search([('product_tmpl_id', '=', templates.id), ('name', '=', templates.company_ids.filtered(lambda c: c.partner_id.default_product_supplier).partner_id.default_product_supplier.id), ('company_id', '=', templates.company_ids.filtered(lambda c: c.partner_id.default_product_supplier).id)]):
                    self.env['product.supplierinfo'].sudo().search([('product_tmpl_id', '=', templates.id), ('name', '=', templates.company_ids.filtered(lambda c: c.partner_id.default_product_supplier).partner_id.default_product_supplier.id), ('company_id', '=', templates.company_ids.filtered(lambda c: c.partner_id.default_product_supplier).id)]).sudo().write({
                        'product_tmpl_id': templates.id,
                        'name': templates.company_ids.filtered(lambda c: c.partner_id.default_product_supplier).partner_id.default_product_supplier.id,
                        'price': templates.list_price * templates.company_ids.filtered(lambda c: c.partner_id.default_product_supplier).partner_id.pourcent_price_product,
                        'company_id': templates.company_ids.filtered(lambda c: c.partner_id.default_product_supplier).id
                    })
                else:
                    self.env['product.supplierinfo'].sudo().create({
                        'product_tmpl_id': templates.id,
                        'name': templates.company_ids.filtered(lambda c: c.partner_id.default_product_supplier).partner_id.default_product_supplier.id,
                        'price': templates.list_price * templates.company_ids.filtered(lambda c: c.partner_id.default_product_supplier).partner_id.pourcent_price_product,
                        'company_id': templates.company_ids.filtered(lambda c: c.partner_id.default_product_supplier).id
                    })

        return templates
