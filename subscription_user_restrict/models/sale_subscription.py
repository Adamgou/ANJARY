# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderTemplate(models.Model):
    _inherit = "sale.order.template"

    user_ids = fields.Many2many(comodel_name="res.users", string="Allowed users")

    @api.model
    def create(self, vals):
        self.clear_caches()
        return super().create(vals)

    def write(self, vals):
        self.clear_caches()
        return super().write(vals)
