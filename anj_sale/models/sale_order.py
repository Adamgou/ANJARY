# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    means_of_payment = fields.Selection(
        [
            ("check", "Check"),
            ("species", "Species"),
            ("mobile_money", "Mobile Money"),
            ("treaty", "Treaty"),
        ],
        string="Means of payment",
        default="mobile_money",
        required=True,
    )