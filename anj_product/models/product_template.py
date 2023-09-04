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

    def _get_default_values_vendor(self):
        default_values = []
        if self.env.company.partner_id.default_product_supplier:
            default_values = [(0, 0, {
                'name': self.env['res.partner'].search([('id', '=', self.env.company.partner_id.default_product_supplier.id)], limit=1),
            })]
        return default_values

    seller_ids = fields.One2many('product.supplierinfo', 'product_tmpl_id', 'Vendors', depends_context=('company',), help="Define vendor pricelists.", default=lambda self: self._get_default_values_vendor())

    @api.onchange('list_price')
    def _change_seller_ids_price(self):
        if self.env.company.partner_id.default_product_supplier:
            self.seller_ids.price = (self.list_price * self.env.company.partner_id.pourcent_price_product)/100



