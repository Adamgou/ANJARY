# coding: utf-8

from odoo import models, fields, api

import re

CLEANR = re.compile("<.*?>")


def clean_html(raw_html):
    cleantext = re.sub(CLEANR, "", raw_html)
    return cleantext


class AccountMove(models.Model):
    _inherit = "account.move"

    partner_sequence = fields.Char(compute="_depends_partner_sequence", store=True)
    partner_codes = fields.Char(readonly=True, related="partner_id.customer_codes")
    period = fields.Char(compute="_compute_period", store=True)
    quit_payment_ids = fields.Many2many(
        "account.payment", string="Payment done", compute="_compute_payment_done"
    )
    compute_field_reset_draft = fields.Boolean(
        string="check field 1", compute="get_user_connect"
    )
    note = fields.Html("Notes")

    @api.depends("compute_field_reset_draft", "user_id")
    def get_user_connect(self):
        self.compute_field_reset_draft = self.env.user.has_group(
            "anj_base.group_to_do_draft"
        ) and self.state in ("posted", "cancel")

    @api.depends()
    def _compute_payment_done(self):
        for rec in self:
            payment_ids = rec._get_reconciled_payments()
            if payment_ids:
                rec.quit_payment_ids = [fields.Command.set(payment_ids.ids)]
            else:
                rec.quit_payment_ids = False

    @api.depends("narration")
    def _compute_period(self):
        for rec in self:
            rec.period = rec.get_period()

    def get_period(self):
        self.ensure_one()
        if not self.narration:
            return ""

        splitted_narration = clean_html(self.narration).split(":")
        if len(splitted_narration) < 2:
            return ""
        return splitted_narration[-1].strip()

    @api.depends(
        "line_ids.amount_currency",
        "line_ids.tax_base_amount",
        "line_ids.tax_line_id",
        "partner_id",
        "line_ids.tax_ids",
        "currency_id",
        "amount_total",
        "amount_untaxed",
        "line_ids.quantity",
        "line_ids.price_subtotal",
    )
    def _compute_tax_totals_json(self):
        return super(AccountMove, self)._compute_tax_totals_json()

    @api.depends("state", "partner_id")
    def _depends_partner_sequence(self):
        for move_id in self.filtered(
            lambda move_id: move_id.state == "posted"
            and move_id.partner_id.invoice_sequence_code
            and move_id.partner_id.invoice_prefix
            and not move_id.partner_sequence
        ):
            move_id.partner_sequence = move_id._get_partner_sequence()

    @api.model
    def _get_partner_sequence(self):
        return self.env["ir.sequence"].next_by_code(
            self.partner_id.invoice_sequence_code
        )

    @api.ondelete(at_uninstall=True)
    def _unlink_update_partner_seq_number_next_actual(self):
        for move_id in self.filtered(
            lambda move_id: move_id.partner_sequence is not False
        ):
            move_id.partner_id.set_to_previous_sequence()
