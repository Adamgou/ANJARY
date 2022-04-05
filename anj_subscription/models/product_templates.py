# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Product_template(models.Model):
    _inherit='product.template'
    
    is_insubscription = fields.Boolean('Is Insubscription')