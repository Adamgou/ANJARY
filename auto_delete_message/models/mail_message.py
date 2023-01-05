# -*- coding: utf-8 -*-

from odoo import models

class MailMessage(models.Model):
    _inherit = 'mail.message'

    def cron_delete_discussion(self):
        records = self.env['mail.message'].search([('model', '=', 'mail.channel'), ('message_type', '=', 'comment')])
        records.unlink()