# -*- coding: utf-8 -*-

from odoo import models, fields, api


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



    def get_sale_order_line_multiline_description_sale(self, product):
        """Add Rental information to the SaleOrderLine name."""
        return super(Inherit_rental_wizard, self).get_location_price(product)

    def get_location_price(self):
        return self.location_price_id.id

    # duration_unit=fields.Selection(selection_add=[
    #     ('half_day', 'Demi-journée '),
    #     ('transfert_day', 'Day transfert'),('transfert_nigth', 'nigth transfert')
    # ], ondelete={'half_day': 'cascade', 'transfert_day': 'cascade', 'transfert_nigth': 'cascade'})