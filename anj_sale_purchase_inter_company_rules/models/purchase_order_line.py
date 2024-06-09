# coding: utf-8

from odoo import models, api


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.model
    def _prepare_purchase_order_line_from_procurement(
        self, product_id, product_qty, product_uom, company_id, values, po
    ):
        res = super()._prepare_purchase_order_line_from_procurement(
            product_id, product_qty, product_uom, company_id, values, po
        )
        if self.env.context.get("from_orderpoint") and self.env.context.get(
            "origin_move_ids"
        ):
            move_id = self.env["stock.move"].search(
                [
                    ("id", "in", self.env.context.get("origin_move_ids")),
                    ("product_id", "=", product_id.id),
                ],
                limit=1,
            )
            if move_id and move_id.sale_line_id:
                res.update({"price_unit": move_id.sale_line_id.price_unit * 0.15})
        return res
