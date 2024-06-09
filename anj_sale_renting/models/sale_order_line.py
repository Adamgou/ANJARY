# coding: utf-8

from odoo import models, fields, api


class Sale_order_line(models.Model):
    _inherit = "sale.order.line"

    location_price_id = fields.Many2one(
        comodel_name="location.price", string="Prix de location", required=False
    )

    selected_lot_ids = fields.Many2many(
        "stock.lot",
        "rental_selected_lot_rel",
        domain="[('product_id','=',product_id)]",
        copy=False,
    )

    @api.onchange("location_price_id")
    def onchange_location_price(self):
        self.price_unit = self.location_price_id.location_price
