# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

DEFAULT_PADDING = 4

class ResPartner(models.Model):
    _inherit = 'res.partner'

    invoice_prefix = fields.Char()
    invoice_sequence_code = fields.Char()
    sequence_started = fields.Boolean(compute='compute_sequence_started')

    @api.constrains('invoice_prefix')
    def _constrains_invoice_prefix(self):
        IrSequence = self.env['ir.sequence']
        for partner_id in self:
            if IrSequence.sudo().search_count([('prefix', '=', partner_id.invoice_prefix)]) > 0:
                raise ValidationError(_('This prefix is aleardy taken, please use another new one.'))

    def compute_sequence_started(self):
        IrSequence = self.env['ir.sequence']
        for partner_id in self:
            if not partner_id.invoice_sequence_code:
                partner_id.sequence_started = False
            else:
                partner_id.sequence_started = IrSequence.sudo().search([('code', '=', partner_id.invoice_sequence_code)])[0].number_next_actual > 1

    @api.model
    def create(self, vals):
        partner_ids = super(ResPartner, self).create(vals)
        filtered_partner_ids = partner_ids.filtered(lambda partner_id: partner_id.invoice_prefix is not False)
        filtered_partner_ids._set_invoice_sequence_code()
        filtered_partner_ids._init_invoice_sequence()
        return partner_ids
    
    def write(self, vals):
        # TODO: in the case if user deleted the sequence prefix
        super(ResPartner, self).write(vals)
        
        if 'invoice_prefix' in vals:
            self.filtered(lambda partner_id: partner_id.invoice_sequence_code is False)._set_invoice_sequence_code()
            self._init_invoice_sequence()
            
    def _init_invoice_sequence(self):
        to_create = []
        for partner_id in self:
            to_create.append({
                'code': partner_id.invoice_sequence_code,
                'prefix': partner_id.invoice_prefix,
                'padding': DEFAULT_PADDING,
                'name': partner_id.invoice_sequence_code
            })
        self.env['ir.sequence'].create(to_create)
    
    def _set_invoice_sequence_code(self):
        for partner_id in self:
            partner_id.invoice_sequence_code = f'{partner_id.name.lower().replace(" ", ".")}-{partner_id.id}'
    
    @api.model
    def set_to_previous_sequence(self):
        sequence_id = self.env['ir.sequence'].sudo().search([('code', '=', self.invoice_sequence_code)])
        sequence_id.number_next_actual -= 1