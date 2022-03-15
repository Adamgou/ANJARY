# -*- coding: utf-8 -*-
# from odoo import http


# class AnjSmsMarketing(http.Controller):
#     @http.route('/anj_sms_marketing/anj_sms_marketing/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/anj_sms_marketing/anj_sms_marketing/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('anj_sms_marketing.listing', {
#             'root': '/anj_sms_marketing/anj_sms_marketing',
#             'objects': http.request.env['anj_sms_marketing.anj_sms_marketing'].search([]),
#         })

#     @http.route('/anj_sms_marketing/anj_sms_marketing/objects/<model("anj_sms_marketing.anj_sms_marketing"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('anj_sms_marketing.object', {
#             'object': obj
#         })
