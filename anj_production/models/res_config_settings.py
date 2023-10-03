# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    number_of_mo = fields.Float(
        string='Number of manufacturing orders', config_parameter="anj_production.number_of_mo",
        required=False, default=2000)
