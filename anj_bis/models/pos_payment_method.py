# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class POsPaymentMethod(models.Model):
    _inherit = "pos.payment.method"

    is_spoon_method = fields.Boolean(string="Spoon")
    is_mvola = fields.Boolean(string="Mvola")
    is_cb = fields.Boolean(string="CB")

    @api.constrains("is_mvola", "is_cb")
    def check_payment_type(self):
        """
        Check if mvola and cb payment is unique
        """
        mvola_payment = (
            self.env["pos.payment.method"]
            .search([("is_mvola", "=", True)])
            .filtered(lambda l: l.id != self.id)
        )
        cb_payment = (
            self.env["pos.payment.method"]
            .search([("is_cb", "=", True)])
            .filtered(lambda l: l.id != self.id)
        )
        if mvola_payment and self.is_mvola:
            raise UserError(_("Mvola payment already exists"))
        if cb_payment and self.is_cb:
            raise UserError(_("CB payment already exists"))
