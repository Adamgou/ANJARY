# -*- coding: utf-8 -*-

from odoo import fields, models


class RentalWizard(models.TransientModel):
    _inherit = 'rental.wizard'

    pickup_date = fields.Datetime(default=lambda _: fields.Datetime.now().replace(
        hour=8, minute=0, second=0, microsecond=0))
    return_date = fields.Datetime(
        default=lambda _: fields.Datetime.now().replace(hour=17, minute=0, second=0, microsecond=0))