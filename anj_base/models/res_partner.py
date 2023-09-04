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

from odoo import api, fields, models, tools, SUPERUSER_ID, _, Command
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




