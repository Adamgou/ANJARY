# coding: utf-8

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    mo_date_from = fields.Datetime(
        string="Production orders from this date will be taken into account when refreshing bom_line quantity",
        config_parameter="anj_production.mo_date_from",
        required=False,
        default=fields.Date.today(),
    )
