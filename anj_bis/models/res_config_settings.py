# coding: utf-8
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    config_logo = fields.Binary(related="pos_config_id.config_logo")
    config_info = fields.Char(related="pos_config_id.config_info")
    config_phone = fields.Char(related="pos_config_id.config_phone")
    config_address = fields.Char(related="pos_config_id.config_address")
