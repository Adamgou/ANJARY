# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class POsPaymentMethod(models.Model):
    _inherit = "pos.payment.method"

    is_mvola = fields.Boolean(string="Mvola")
    is_cb = fields.Boolean(string="CB")

    @api.constrains("is_mvola", "is_cb")
    def check_payment_type(self):
        """
        Check if mvola and cb payment is unique
        """
        for payment in self:
            if payment.is_mvola and payment.is_cb:
                raise UserError(
                    _("Payment method can't be mvola and cb in the same time")
                )
