# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleSubscription(models.Model):
    _inherit = 'sale.subscription.template'

    user_ids = fields.Many2many(comodel_name='res.users', string='Allowed users')

    @api.model
    def create(self, vals):
        self.clear_caches()
        return super(SaleSubscription, self).create(vals)

    def write(self, vals):
        self.clear_caches()
        return super(SaleSubscription, self).write(vals)

class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def get_allowed_subscription(self):
        return self.env['sale.subscription.template'].search([]).filtered(lambda template_id: not template_id.user_ids or self.id in template_id.user_ids.ids).ids