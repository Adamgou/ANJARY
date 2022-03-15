# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class anj_sms_marketing(models.Model):
#     _name = 'anj_sms_marketing.anj_sms_marketing'
#     _description = 'anj_sms_marketing.anj_sms_marketing'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
