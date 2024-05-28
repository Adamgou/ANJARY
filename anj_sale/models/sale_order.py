# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    means_of_payment = fields.Selection(
        [
            ("check", "Check"),
            ("species", "Species"),
            ("mobile_money", "Mobile Money"),
            ("treaty", "Treaty"),
        ],
        string="Means of payment",
        default="mobile_money",
        required=True,
    )

    note_client = fields.Char(string="Note")

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        stock_picking = self.env["stock.picking"].search(
            [("id", "=", self.picking_ids.id)]
        )
        for moves in stock_picking.move_ids_without_package:
            moves.write({"quantity": moves.product_uom_qty})
        return res

    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        res["note_client"] = self.note_client
        return res
