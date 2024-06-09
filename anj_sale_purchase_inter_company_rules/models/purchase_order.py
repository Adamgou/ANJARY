# coding: utf-8

from odoo import models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def inter_company_create_sale_order(self, company):
        """Auto validate the transfers."""
        super().inter_company_create_sale_order(company)
        self.env["sale.order"].sudo().search(
            [("auto_purchase_order_id", "in", self.ids), ("auto_generated", "=", True)]
        ).picking_ids.sudo().button_validate()
