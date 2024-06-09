# coding: utf-8

from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    global_discount_type = fields.Selection(
        string="Global Discount Type",
        selection=[
            ("percentage", "Percentage"),
            ("amount", "Amount"),
            ("both", "Both"),
        ],
        default="percentage",
    )
