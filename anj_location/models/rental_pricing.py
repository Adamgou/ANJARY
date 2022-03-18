# -*- coding: utf-8 -*-

from odoo import models, fields, api

# PERIOD_RATIO = {
#     'hour': 1,
#     'day': 10,
#     'nigth': 6,
#     'transfert_day': 1,
#     'transfert_nigth': 1,
#     'week': 24 * 7
# }
class Rental_pricing(models.Model):

    _inherit="rental.pricing"

    location_price_id = fields.Many2one(
        comodel_name='location.price',
        string='Location price',
        required=True)


#     unit = fields.Selection(selection_add=[
#         ('half_day', 'Demi-journée '),
#         ('transfert_day', 'Day transfert'),('transfert_nigth', 'nigth transfert')
#     ], ondelete={'half_day': 'set default', 'transfert_day': 'set default', 'transfert_nigth': 'set default'})
#
#     @api.model
#     def _compute_duration_vals(self,pickup_date, return_date):
#         res = super(Rental_pricing, self)._compute_duration_vals(pickup_date, return_date)
#         res.update( [('half_day', 6),('transfert_day',1),('transfert_nigth',1)])
#         return res
#
#     @api.onchange('unit')
#     def onchange_method(self):
#         if self.unit=='day':
#             self.price=150000
#         elif self.unit=='half_day':
#             self.price=100000
#         elif self.unit=='transfert_day':
#             self.price=70000
#         elif self.unit=='transfert_nigth':
#             self.price=80000



class Inherit_rental_wizard(models.TransientModel):
    _inherit='rental.wizard'
    location_price_id = fields.Many2one(
        comodel_name='location.price',
        string='Location price',
        store=True,
        required=True)

    location_price = fields.Float(
        string='Price',
        store=True,
        readonly=True)

    @api.onchange('location_price_id')
    def onchange_location_price_id(self):
        for data in self:
            data.unit_price=data.location_price_id.location_price*data.duration
            data.location_price=data.location_price_id.location_price
        




    # duration_unit=fields.Selection(selection_add=[
    #     ('half_day', 'Demi-journée '),
    #     ('transfert_day', 'Day transfert'),('transfert_nigth', 'nigth transfert')
    # ], ondelete={'half_day': 'cascade', 'transfert_day': 'cascade', 'transfert_nigth': 'cascade'})