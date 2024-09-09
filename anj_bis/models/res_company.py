# coding: utf-8

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    is_biskot = fields.Boolean(help="Used on POS when managing spoon products")
