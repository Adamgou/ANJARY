# -*- config: utf-8 -*-


from odoo import models, fields


class PosConfig(models.Model):
    _inherit = "pos.config"

    config_logo = fields.Binary(string="Config Logo", readonly=False)
    config_info = fields.Char(string="Config info")
    config_phone = fields.Char(string="Config phone")
    config_address = fields.Char(string="Config address")
