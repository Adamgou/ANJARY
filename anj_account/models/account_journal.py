# -*- coding: utf-8 -*-

from odoo import models, fields

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    no_header = fields.Boolean(default=False)