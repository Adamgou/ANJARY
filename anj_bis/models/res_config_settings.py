# coding: utf-8
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    config_logo = fields.Binary(ralted="pos_config_id.config_logo")
    config_info = fields.Char(ralted="pos_config_id.config_info")
    config_phone = fields.Char(ralted="pos_config_id.config_phone")
    config_address = fields.Char(ralted="pos_config_id.config_address")
