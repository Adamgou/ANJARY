# coding: utf-8

from odoo import models, _


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    def button_mark_done(self):
        res = super().button_mark_done()
        date_from = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("anj_production.mo_date_from")
        )

        last_production_ids = self.search(
            [("create_date", ">=", date_from), ("bom_id", "=", self.bom_id.id)],
            order="create_date desc",
        )
        BOMLine = self.env["mrp.bom.line"]
        for move_id in self.move_raw_ids.filtered(
            lambda move: not move.bom_line_id
            and move.product_id.id
            not in self.bom_id.bom_line_ids.mapped("product_id").ids
        ):
            new_line_id = BOMLine.create(
                {
                    "bom_id": self.bom_id.id,
                    "product_id": move_id.product_id.id,
                    "product_qty": move_id.forecast_availability,
                    "product_uom_id": move_id.product_uom.id,
                }
            )
            move_id.bom_line_id = new_line_id.id

        self.bom_id.bom_line_ids.filtered(
            lambda bom_line: bom_line.id
            not in self.move_raw_ids.mapped("bom_line_id").ids
        ).unlink()

        qty_producing_total = sum(last_production_ids.mapped("qty_producing"))
        if qty_producing_total:
            for line_id in self.bom_id.bom_line_ids:
                line_id.write(
                    {
                        "product_qty": sum(
                            last_production_ids.mapped("move_raw_ids")
                            .filtered(
                                lambda move: move.product_id == line_id.product_id
                            )
                            .mapped("quantity")
                        )
                        / qty_producing_total
                    }
                )

        return res
