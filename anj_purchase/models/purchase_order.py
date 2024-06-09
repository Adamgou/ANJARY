# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def button_approve(self, force=False):
        res = super().button_approve(force)
        sale_order_ids = self.env["sale.order"].search(
            [("auto_purchase_order_id", "in", self.ids)]
        )
        so_picking_ids = sale_order_ids.mapped("picking_ids")
        if so_picking_ids:
            so_picking_ids.button_validate()
        return res

    def button_confirm(self):
        res = super().button_confirm()
        picking_ids_to_validate = self.mapped("picking_ids")
        if picking_ids_to_validate:
            picking_ids_to_validate.button_validate()
        return True
