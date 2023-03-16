# -*- coding: utf-8 -*-

from odoo import models, fields


class MailChannel(models.Model):
    _inherit = "mail.channel"

    message_lifetime = fields.Integer(default=1, required=True)
    interval_type = fields.Selection(
        [("days", "Days"), ("weeks", "Weeks"), ("months", "Months")],
        default="days",
        required=True,
    )
    is_message_deletion_active = fields.Boolean(default=False)
