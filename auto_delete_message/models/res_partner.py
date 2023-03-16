# -*- coding: utf-8 -*-

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_message_deletion_active = fields.Boolean()
    message_lifetime = fields.Integer(default=1, required=True)
    interval_type = fields.Selection(
        [('days', 'Days'), ('weeks', 'Weeks'), ('months', 'Months')], default='days', required=True)