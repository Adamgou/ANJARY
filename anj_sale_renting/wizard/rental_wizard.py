# -*- coding: utf-8 -*-

from odoo import fields, models, api

from datetime import timedelta

LOCATION_INTERVAL = {
    'journey': (5, 15),
    'evening': (15, 21),
    'night': (15, 4),
}


class RentalWizard(models.TransientModel):
    _inherit = 'rental.wizard'

    pickup_date = fields.Datetime(default=lambda _: fields.Datetime.now().replace(
        hour=8, minute=0, second=0, microsecond=0))
    return_date = fields.Datetime(
        default=lambda _: fields.Datetime.now().replace(hour=17, minute=0, second=0, microsecond=0))

    @api.onchange('location_price_id')
    def _onchange_location_price_id(self):
        if self.location_price_id:
            if self.location_price_id.id == self.env.ref('anj_sale_renting.journey_price').id:
                location_interval = LOCATION_INTERVAL.get('journey')
            elif self.location_price_id.id == self.env.ref('anj_sale_renting.evening_price').id:
                location_interval = LOCATION_INTERVAL.get('evening')
            else:
                location_interval = LOCATION_INTERVAL.get('night')
            self.pickup_date = self.pickup_date.replace(
                hour=location_interval[0], minute=0, second=0, microsecond=0)
            day = (self.pickup_date +
                   timedelta(days=1 if location_interval[1] <= location_interval[0] else 0)).day
            self.return_date = self.return_date.replace(
                day=day, hour=location_interval[1], minute=0, second=0, microsecond=0)
