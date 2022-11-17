# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import datetime
import calendar

from dateutil.relativedelta import relativedelta
from markupsafe import Markup
from datetime import date

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import format_date, is_html_empty

_logger = logging.getLogger(__name__)

INTERVAL_FACTOR = {
    "daily": 30.0,
    "weekly": 30.0 / 7.0,
    "monthly": 1.0,
    "yearly": 1.0 / 12.0,
}

PERIODS = {"daily": "days", "weekly": "weeks",
           "monthly": "months", "yearly": "years"}


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    prorata = fields.Boolean(default=True)
    is_monthly = fields.Boolean(compute='compute_is_monthly', store=True)
    can_read_move = fields.Boolean(
        default=lambda self: self.env['account.move'].check_access_rights('read', raise_exception=False))

    @api.depends('template_id.recurring_rule_type')
    def compute_is_monthly(self):
        for sale_sub in self:
            sale_sub.is_monthly = sale_sub.template_id.recurring_rule_type == 'monthly'

    @api.constrains('prorata')
    def _contrains_prorata(self):
        for sale_subscription in self:
            if sale_subscription.can_read_move and sale_subscription.invoice_count > 0:
                raise UserError(
                    _('Sorry, there is already invoice for this sale subscription!'))
            elif not sale_subscription.can_read_move:
                raise UserError(
                    _('Sorry, you do not have access right for this operation!'))

    @api.model
    def _get_recurring_next_date(self, interval_type, interval, current_date, recurring_invoice_day):
        if self.prorata and interval_type == 'monthly' and (current_date == self.date_start or current_date.day == 1):
            return current_date.replace(day=1) + relativedelta(months=1)

        return super(SaleSubscription, self)._get_recurring_next_date(interval_type, interval, current_date, recurring_invoice_day)

    def _prepare_invoice_data(self):
        self.ensure_one()
        if not self.prorata:
            return super(SaleSubscription, self)._prepare_invoice_data()

        if not self.partner_id:
            raise UserError(
                _("You must first select a Customer for Subscription %s!", self.name)
            )

        company = self.env.company or self.company_id

        journal = self.template_id.journal_id or self.env["account.journal"].search(
            [("type", "=", "sale"), ("company_id", "=", company.id)], limit=1
        )
        if not journal:
            raise UserError(
                _('Please define a sale journal for the company "%s".')
                % (company.name or "",)
            )

        next_date = self.recurring_next_date
        if self.prorata and self.template_id.recurring_rule_type == "monthly":
            begin_date = (
                self.date_start
                if self.date_start.month == self.recurring_next_date.month
                else date(
                    self.recurring_next_date.year, self.recurring_next_date.month, 1
                )
            )
        else:
            begin_date = next_date

        if not next_date:
            raise UserError(
                _('Please define Date of Next Invoice of "%s".') % (
                    self.display_name,)
            )
        recurring_next_date = self._get_recurring_next_date(
            self.recurring_rule_type,
            self.recurring_interval,
            next_date,
            self.recurring_invoice_day,
        )
        # remove 1 day as normal people thinks in term of inclusive ranges.
        end_date = fields.Date.from_string(
            recurring_next_date) - relativedelta(days=1)
        addr = self.partner_id.address_get(["delivery", "invoice"])
        sale_order = self.env["sale.order"].search(
            [("order_line.subscription_id", "in", self.ids)], order="id desc", limit=1
        )
        use_sale_order = sale_order and sale_order.partner_id == self.partner_id
        partner_id = (
            sale_order.partner_invoice_id.id
            if use_sale_order
            else self.partner_invoice_id.id or addr["invoice"]
        )
        partner_shipping_id = (
            sale_order.partner_shipping_id.id
            if use_sale_order
            else self.partner_shipping_id.id or addr["delivery"]
        )
        fpos = (
            self.env["account.fiscal.position"]
            .with_company(company)
            .get_fiscal_position(self.partner_id.id, partner_shipping_id)
        )
        narration = _("This invoice covers the following period: %s - %s") % (
            format_date(self.env, begin_date),
            format_date(self.env, end_date),
        )
        if not is_html_empty(self.description):
            narration += Markup("<br/>") + self.description
        elif self.env["ir.config_parameter"].sudo().get_param(
            "account.use_invoice_terms"
        ) and not is_html_empty(self.company_id.invoice_terms):
            narration += Markup("<br/>") + self.company_id.invoice_terms
        res = {
            "move_type": "out_invoice",
            "partner_id": partner_id,
            "partner_shipping_id": partner_shipping_id,
            "currency_id": self.pricelist_id.currency_id.id,
            "journal_id": journal.id,
            "invoice_origin": self.code,
            "fiscal_position_id": fpos.id,
            "invoice_payment_term_id": self.payment_term_id.id,
            "narration": narration,
            "invoice_user_id": self.user_id.id,
            "partner_bank_id": company.partner_id.bank_ids.filtered(
                lambda b: not b.company_id or b.company_id == company
            )[:1].id,
        }
        if self.team_id:
            res["team_id"] = self.team_id.id
        return res

    def _prepare_invoice_line(self, line, fiscal_position, date_start=False, date_stop=False):
        company = self.env.company or line.analytic_account_id.company_id
        tax_ids = line.product_id.taxes_id.filtered(
            lambda t: t.company_id == company)
        if fiscal_position and tax_ids:
            tax_ids = self.env['account.fiscal.position'].browse(
                fiscal_position).map_tax(tax_ids)
            line.price_unit = self.env['account.tax']._fix_tax_included_price_company(
                line.price_unit, line.product_id.taxes_id, tax_ids, self.company_id)
        return {
            'name': line.name,
            'subscription_id': line.analytic_account_id.id,
            'price_unit': line.price_unit or 0.0,
            'discount': line.discount,
            'quantity': self._get_quantity_prorata(line.quantity, date_start, date_stop) if self.prorata and self.template_id.recurring_rule_type == 'monthly' else line.quantity,
            'product_uom_id': line.uom_id.id,
            'product_id': line.product_id.id,
            'tax_ids': [(6, 0, tax_ids.ids)],
            'analytic_account_id': line.analytic_account_id.analytic_account_id.id,
            'analytic_tag_ids': [(6, 0, line.analytic_account_id.tag_ids.ids)],
            'subscription_start_date': date_start,
            'subscription_end_date': date_stop,
        }

    def _prepare_invoice_lines(self, fiscal_position):
        self.ensure_one()
        if not self.prorata or self.template_id.recurring_rule_type != 'monthly':
            return super(SaleSubscription, self)._prepare_invoice_lines(fiscal_position)

        if self.template_id:
            revenue_date_start = self.recurring_next_date
            revenue_date_stop = self._get_recurring_next_date(
                self.recurring_rule_type,
                self.recurring_interval,
                self.recurring_next_date,
                self.recurring_invoice_day,
            ) - relativedelta(days=1)
            return [
                (
                    0,
                    0,
                    self._prepare_invoice_line(
                        line, fiscal_position, revenue_date_start, revenue_date_stop
                    ),
                )
                for line in self.recurring_invoice_line_ids
            ]
        else:
            return super(SaleSubscription, self)._prepare_invoice_lines(fiscal_position)

    def _get_quantity_prorata(self, quantity, date_from, date_to):
        output = quantity
        if date_from.month == date_to.month and date_from.year == date_to.year:
            number_of_days = (date_to - date_from).days + 1
            month_range = calendar.monthrange(
                date_to.year, date_from.month)[1]
            if number_of_days != month_range:
                output = (number_of_days / month_range) + (
                    quantity - 1
                    if quantity > 0
                    else quantity
                )
        return output
