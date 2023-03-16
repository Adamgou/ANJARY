# -*- coding: utf-8 -*-

from odoo import models
from datetime import date
from dateutil.relativedelta import relativedelta

TO_DATE = {
    'days': lambda x: date.today() - relativedelta(days=x),
    'weeks': lambda x: date.today() - relativedelta(days=7*x),
    'months': lambda x: date.today() - relativedelta(months=x),
}


class MailMessage(models.Model):
    _inherit = 'mail.message'

    def cron_delete_discussion(self):
        partner_ids = self.env['res.partner'].search(
            [('is_message_deletion_active', '=', True)])
        MailMessage = self.env['mail.message']
        channel_ids = self.env['mail.channel'].search([]).filtered(
            lambda channel: channel.member_count > 2)

        for partner_id in partner_ids:
            records = MailMessage.search([('model', '=', 'mail.channel'), ('res_id', 'not in', channel_ids.mapped('id')), ('author_id', '=', partner_id.id), (
                'date', '<=', TO_DATE[partner_id.interval_type](partner_id.message_lifetime))])
            records.unlink()

        for channel_id in channel_ids.filtered(lambda channel: channel.is_message_deletion_active):
            records = MailMessage.search([('model', '=', 'mail.channel'), ('res_id', '=', channel_id.id), (
                'date', '<=', TO_DATE[channel_id.interval_type](channel_id.message_lifetime))])
            records.unlink()