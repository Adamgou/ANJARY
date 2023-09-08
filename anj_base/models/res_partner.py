# -*- coding: utf-8 -*-


import base64
import collections
import datetime
import hashlib
import pytz
import threading
import re

import requests
from collections import defaultdict
from lxml import etree
from random import randint
from werkzeug import urls

from odoo import api, fields, models, tools, SUPERUSER_ID, _, Command, exceptions
from odoo.osv.expression import get_unaccent_wrapper
from odoo.exceptions import RedirectWarning, UserError, ValidationError

class Partner(models.Model):

    _inherit = 'res.partner'

    is_product_supplier = fields.Boolean()
    pourcent_price_product = fields.Float()
    default_product_supplier = fields.Many2one('res.partner')

    @api.depends('default_product_supplier')
    def get_pourcent_price_product(self):
        for partner in self:
            if partner.default_product_supplier:
                partner.is_product_supplier = True
            else:
                partner.is_product_supplier = False

    @api.constrains('is_product_supplier')
    def checked_is_product_supplier(self):
        checked_is_product_supplier = self.search([('id', '!=', self.id), ('is_product_supplier', '=', True)], limit=1)
        if self.is_product_supplier and checked_is_product_supplier:
            raise exceptions.ValidationError(_('Un contact à déjàt un fournisseur par défaut'))



