# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime


class MailChannel(models.Model):
    _inherit = 'mail.channel'

    message_lifetime = fields.Integer(default=1, required=True)
    interval_type = fields.Selection(
        [('days', 'Days'), ('weeks', 'Weeks'), ('months', 'Months')], default='days', required=True)
    is_message_deletion_active = fields.Boolean(default=False)

    # ir_cron_id = fields.Many2one(comodel_name='ir.cron')

    # @api.model
    # def create(self, vals):
    #     channel_ids = super(MailChannel, self).create(vals)
    #     self.auto_create_cron(create=True)
    #     return channel_ids

    # def auto_create_cron(self):
    #     for channel_id in self:
    #         ir_cron_dict = {
    #             'name': _('Auto delete: {}').format(channel_id.name),
    #             'interval_number': channel_id.interval_number,
    #             'interval_type': channel_id.interval_type,
    #             'nextcall': channel_id.nextcall,
    #             'active': channel_id.is_cron_active,
    #             'numbercall': -1,
    #             'model_id': self.env['ir.model'].sudo().search([('model', '=', self._name)]).id,
    #             'state': 'code',
    #             'code': f'model.cron_delete_discussion({channel_id.id})'
    #         }
    #         channel_id.ir_cron_id = self.env['ir.cron'].create(ir_cron_dict).id

    # def auto_update_cron(self):
    #     for channel_id in self:
    #         ir_cron_dict = {
    #             'name': _('Auto delete: {}').format(channel_id.name),
    #             'interval_number': channel_id.interval_number,
    #             'interval_type': channel_id.interval_type,
    #             'numbercall': -1,
    #             'active': channel_id.is_cron_active,
    #             'state': 'code',
    #             'code': f'model.cron_delete_discussion({channel_id.id})'
    #         }
    #         if channel_id.ir_cron_id:
    #             channel_id.ir_cron_id.write(ir_cron_dict)
    #         else:
    #             channel_id.auto_create_cron()

    # def write(self, vals):
    #     super(MailChannel, self).write(vals)
    #     self.auto_update_cron()

    # def cron_delete_discussion(self, channel_id):
    #     self = self.env[self._name].browse(channel_id)
    #     message_to_delete = self.env['mail.message'].search(
    #         [('id', 'in', self.message_ids.ids)])
    #     message_to_delete.unlink()
