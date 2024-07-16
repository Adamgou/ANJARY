# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class ProductTemplate(models.Model):
    _inherit = "product.template"

    rented = fields.Boolean(string="Rented", compute="_compute_product_rented")
    partner_id = fields.Many2one(
        "res.partner", string="Partner", compute="_compute_product_rented"
    )
    subscription = fields.Many2one(
        "sale.order", string="N° subscription", compute="_compute_product_rented"
    )

    @api.depends("company_id")
    def _compute_product_rented(self):
        SaleOrder = self.env["sale.order"]
        for product in self:
            product.rented = False
            product.partner_id = False
            product.subscription = False
            if product.env.company.name.lower().startswith("societe immobiliere"):
                sale_subscription = SaleOrder.search(
                    [
                        ("is_subscription", "=", True),
                        ("state", "in", ["sale", "done"]),
                        ("subscription_state", "=", "3_progress"),
                    ]
                )
                for order in sale_subscription:
                    if order.order_line.filtered(
                        lambda l: l.product_id.product_tmpl_id == product
                    ):
                        product.rented = True
                        product.partner_id = order.partner_id
                        product.subscription = order
                        break
                    else:
                        product.rented = False
