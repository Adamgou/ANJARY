# coding: utf-8

from datetime import timedelta

from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _unavailability_period(self, fro, to):
        """Give unavailability period given rental period."""
        return fro - timedelta(hours=self.preparation_time), to

    def _get_unavailable_qty_and_lots(self, fro, to, **kwargs):
        """
        :param datetime fro:
        :param datetime to:
        :param dict kwargs: search domain restrictions (ignored_soline_id, warehouse_id)
        :return tuple(float, array(stock.production.lot)):
        """

        def unavailable_qty(so_line):
            return so_line.product_uom_qty - so_line.qty_returned

        begins_during_period, ends_during_period, covers_period = (
            self._get_active_rental_lines(fro, to, **kwargs)
        )
        active_lines_in_period = begins_during_period + ends_during_period
        max_qty_rented = 0

        # TODO is it more efficient to filter the records active in period
        # or to make another search on all the sale order lines???
        if active_lines_in_period:
            for date in [fro] + begins_during_period.mapped("reservation_begin"):
                active_lines_at_date = active_lines_in_period.filtered(
                    lambda line: line.reservation_begin <= date
                    and line.return_date >= date
                )
                qty_rented_at_date = sum(active_lines_at_date.mapped(unavailable_qty))
                max_qty_rented = max(max_qty_rented, qty_rented_at_date)

        qty_always_in_rent_during_period = sum(covers_period.mapped(unavailable_qty))

        # returns are removed from the count (WARNING : early returns don't support padding times)
        all_lines = active_lines_in_period + covers_period
        rented_serial_during_period = all_lines.mapped("unavailable_lot_ids")

        return (
            max_qty_rented + qty_always_in_rent_during_period,
            rented_serial_during_period,
        )
