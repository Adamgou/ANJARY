# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class anj_social_marketing(models.Model):
#     _name = 'anj_social_marketing.anj_social_marketing'
#     _description = 'anj_social_marketing.anj_social_marketing'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
