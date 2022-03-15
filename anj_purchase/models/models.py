# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class anj_purchase(models.Model):
#     _name = 'anj_purchase.anj_purchase'
#     _description = 'anj_purchase.anj_purchase'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
