# -*- coding: utf-8 -*-

from odoo import models, fields

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    no_header = fields.Boolean(default=False)
    is_customer_journal = fields.Boolean(default=False)
    no_footer = fields.Boolean(default=False)