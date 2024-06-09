# coding: utf-8

from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _trigger_scheduler(self):
        """Letting move_ids to be known for the next methods in callstack.
        We need those moves for example: to udpate some fields on po_line
        based on move's fields
        """
        return super(
            StockMove, self.with_context(origin_move_ids=self.ids)
        )._trigger_scheduler()
