from odoo import models, fields, api
class Sale_order_line(models.Model):
    _inherit="sale.order.line"
    location_price_id = fields.Many2one(
        comodel_name='location.price',
        string='Location price',
        required=False)

    @api.onchange('location_price_id')
    def onchange_location_price(self):
        self.price_unit=self.location_price_id.location_price
