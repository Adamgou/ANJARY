# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, Command, fields, models



class AccountPayment(models.Model):
    _inherit = 'account.payment'


    # invoice_registration_ids = fields.Many2many('account.move', string="Reconciled Invoices",
    #                                             compute='_compute_invoice_registration_ids',
    #                                             help="Invoices whose journal items have been reconciled with these payments.")
    #
    # # @api.depends('move_id.line_ids.matched_debit_ids', 'move_id.line_ids.matched_credit_ids')
    # def _compute_invoice_registration_ids(self):
    #     stored_payments = self.filtered('id')
    #
    #     self._cr.execute('''
    #         SELECT
    #             payment.id,
    #             ARRAY_AGG(DISTINCT invoice.id) AS invoice_ids,
    #             invoice.move_type
    #         FROM account_payment payment
    #         JOIN account_move move ON move.id = payment.move_id
    #         JOIN account_move_line line ON line.move_id = move.id
    #         JOIN account_partial_reconcile part ON
    #             part.debit_move_id = line.id
    #             OR
    #             part.credit_move_id = line.id
    #         JOIN account_move_line counterpart_line ON
    #             part.debit_move_id = counterpart_line.id
    #             OR
    #             part.credit_move_id = counterpart_line.id
    #         JOIN account_move invoice ON invoice.id = counterpart_line.move_id
    #         JOIN account_account account ON account.id = line.account_id
    #         WHERE account.internal_type IN ('receivable', 'payable')
    #             AND payment.id IN %(payment_ids)s
    #             AND line.id != counterpart_line.id
    #             AND invoice.move_type in ('out_invoice', 'out_refund', 'in_invoice', 'in_refund', 'out_receipt', 'in_receipt')
    #         GROUP BY payment.id, invoice.move_type
    #     ''', {
    #         'payment_ids': tuple(stored_payments.ids)
    #     })
    #     query_res = self._cr.dictfetchall()
    #
    #     for res in query_res:
    #         pay = self.browse(res['id'])
    #         if res['move_type'] in self.env['account.move'].get_sale_types(True):
    #             model_b_ids = self.env['account.move'].search([('id', '=', res.get('invoice_ids', []))])
    #             self.write({'invoice_registration_ids': [(4, model_b_id.id) for model_b_id in model_b_ids]})
    #         else:
    #             model_b_ids = self.env['account.move'].search([('id', '=', res.get('invoice_ids', []))])
    #             self.write({'invoice_registration_ids': [(4, model_b_id.id) for model_b_id in model_b_ids]})

