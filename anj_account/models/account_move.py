from odoo import models, api


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.depends(
        "line_ids.amount_currency",
        "line_ids.tax_base_amount",
        "line_ids.tax_line_id",
        "partner_id",
        "currency_id",
        "amount_total",
        "amount_untaxed",
        "line_ids.quantity",
        "line_ids.price_subtotal",
    )
    def _compute_tax_totals_json(self):
        return super(AccountMove, self)._compute_tax_totals_json()
