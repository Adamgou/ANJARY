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
    'daily': 30.0,
    'weekly': 30.0 / 7.0,
    'monthly': 1.0,
    'yearly': 1.0 / 12.0,
}

PERIODS = {'daily': 'days', 'weekly': 'weeks',
           'monthly': 'months', 'yearly': 'years'}


class SaleSubscription(models.Model):
    _inherit = "sale.subscription"

    def _prepare_invoice_data(self):
        self.ensure_one()

        if not self.partner_id:
            raise UserError(
                _("You must first select a Customer for Subscription %s!", self.name))

        company = self.env.company or self.company_id

        journal = self.template_id.journal_id or self.env['account.journal'].search(
            [('type', '=', 'sale'), ('company_id', '=', company.id)], limit=1)
        if not journal:
            raise UserError(_('Please define a sale journal for the company "%s".') % (
                company.name or '', ))

        next_date = self.recurring_next_date
        if self.template_id.recurring_rule_type == 'monthly':
            begin_date = self.date_start if self.date_start.month == self.recurring_next_date.month else date(
                self.recurring_next_date.year, self.recurring_next_date.month, 1)
        else:
            begin_date = next_date
        if not next_date:
            raise UserError(
                _('Please define Date of Next Invoice of "%s".') % (self.display_name,))
        recurring_next_date = self._get_recurring_next_date(
            self.recurring_rule_type, self.recurring_interval, next_date, self.recurring_invoice_day)
        # remove 1 day as normal people thinks in term of inclusive ranges.
        end_date = fields.Date.from_string(
            recurring_next_date) - relativedelta(days=1)
        if self.template_id.recurring_rule_type == 'monthly':
            end_date = self.recurring_next_date
        addr = self.partner_id.address_get(['delivery', 'invoice'])
        sale_order = self.env['sale.order'].search(
            [('order_line.subscription_id', 'in', self.ids)], order="id desc", limit=1)
        use_sale_order = sale_order and sale_order.partner_id == self.partner_id
        partner_id = sale_order.partner_invoice_id.id if use_sale_order else self.partner_invoice_id.id or addr[
            'invoice']
        partner_shipping_id = sale_order.partner_shipping_id.id if use_sale_order else self.partner_shipping_id.id or addr[
            'delivery']
        fpos = self.env['account.fiscal.position'].with_company(
            company).get_fiscal_position(self.partner_id.id, partner_shipping_id)
        narration = _("This invoice covers the following period: %s - %s") % (
            format_date(self.env, begin_date), format_date(self.env, end_date))
        if not is_html_empty(self.description):
            narration += Markup('<br/>') + self.description
        elif self.env['ir.config_parameter'].sudo().get_param('account.use_invoice_terms') and not is_html_empty(self.company_id.invoice_terms):
            narration += Markup('<br/>') + self.company_id.invoice_terms
        res = {
            'move_type': 'out_invoice',
            'partner_id': partner_id,
            'partner_shipping_id': partner_shipping_id,
            'currency_id': self.pricelist_id.currency_id.id,
            'journal_id': journal.id,
            'invoice_origin': self.code,
            'fiscal_position_id': fpos.id,
            'invoice_payment_term_id': self.payment_term_id.id,
            'narration': narration,
            'invoice_user_id': self.user_id.id,
            'partner_bank_id': company.partner_id.bank_ids.filtered(lambda b: not b.company_id or b.company_id == company)[:1].id,
        }
        if self.team_id:
            res['team_id'] = self.team_id.id
        return res

    def _prepare_invoice_lines(self, fiscal_position):
        self.ensure_one()
        if self.template_id and self.template_id.recurring_rule_type == 'monthly':
            revenue_date_stop = self.recurring_next_date
            revenue_date_start = self.date_start if self.date_start.month == self.recurring_next_date.month else date(
                self.recurring_next_date.year, self.recurring_next_date.month, 1)
            return [(0, 0, self._prepare_invoice_line(line, fiscal_position, revenue_date_start, revenue_date_stop)) for line in self.recurring_invoice_line_ids]
        else:
            return super(SaleSubscription, self)._prepare_invoice_lines(fiscal_position)


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def create(self, vals_list):
        """"Update quantity fields of line."""

        account_move_ids = super(AccountMove, self).create(vals_list)

        for line_id in account_move_ids.mapped('line_ids'):
            if line_id.subscription_id and line_id.subscription_id.template_id.recurring_rule_type == 'monthly' and line_id.subscription_start_date and line_id.subscription_end_date:
                date_from = line_id.subscription_start_date
                date_to = line_id.subscription_end_date
                if date_from.month == date_to.month:
                    number_of_days = (date_to - date_from).days + 1
                    month_range = calendar.monthrange(
                        date_to.year, date_from.month)[1]
                    if number_of_days != month_range:
                        line_id.quantity = (number_of_days / month_range) + (
                            line_id.quantity - 1 if line_id.quantity > 0 else line_id.quantity)

        return account_move_ids
