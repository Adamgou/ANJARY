# coding: utf-8

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    number_of_mo = fields.Float(
        string="Number of manufacturing orders",
        config_parameter="anj_production.number_of_mo",
        required=False,
        default=2000,
    )
