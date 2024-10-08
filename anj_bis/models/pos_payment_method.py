# -*- coding: utf-8 -*-

from odoo import models, fields


class POsPaymentMethod(models.Model):
    _inherit = "pos.payment.method"

    is_spoon_method = fields.Boolean(string="Spoon")
    is_mvola = fields.Boolean(string="Mvola")
    is_cb = fields.Boolean(string="CB")
