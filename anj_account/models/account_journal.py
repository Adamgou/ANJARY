# -*- coding: utf-8 -*-

from odoo import models, fields

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    with_logo = fields.Boolean(default=True)