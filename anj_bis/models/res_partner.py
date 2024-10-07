# -*- config: utf-8 -*-

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_checking_partner = fields.Boolean(string="Checking partner")
