# coding: utf-8

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    delivery_no_create_button = fields.Boolean(
        help="Hide create button when accessing delivery from sale order."
    )
