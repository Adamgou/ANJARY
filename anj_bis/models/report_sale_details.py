# coding: utf-8

from odoo import models, fields, api


class ReportSaleDetails(models.AbstractModel):
    _inherit = "report.point_of_sale.report_saledetails"

    @api.model
    def get_sale_details(
        self, date_start=False, date_stop=False, config_ids=False, session_ids=False
    ):
        out = super().get_sale_details(date_start, date_stop, config_ids, session_ids)
        categories = out.get("products")
        product_ids = []
        for categ in categories:
            products = categ.get("products")
            for product in products:
                product_ids.append(product.get("product_id"))
        products = self.env["product.product"].search(
            [("id", "in", product_ids), ("spoon", "=", True)]
        )
        spoons = products.mapped("id")

        out.update({"spoons": spoons})

        spoons_data = []
        removed = 0
        for categ in categories:
            categ_products = categ.get("products")
            spoon_category = {"name": "", "qty": 0.0, "total": 0.0, "products": []}
            fake_products = categ_products.copy()
            for i, product in enumerate(fake_products):
                if product.get("product_id") in spoons:
                    spoon_category["name"] = categ.get("name")
                    spoon_category["products"].append({**product})
                    spoon_category["total"] += product.get("base_amount")
                    spoon_category["qty"] += product.get("quantity")
                    categ["qty"] -= product["quantity"]
                    categ["total"] -= product["base_amount"]
                    categ_products.pop(i - removed)
                    removed += 1
            if spoon_category.get("products"):
                spoons_data.append(spoon_category)

        out.update({"spoons_data": spoons_data})
        return out
