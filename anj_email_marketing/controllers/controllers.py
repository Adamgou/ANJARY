# -*- coding: utf-8 -*-
# from odoo import http


# class AnjEmailMarketing(http.Controller):
#     @http.route('/anj_email_marketing/anj_email_marketing/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/anj_email_marketing/anj_email_marketing/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('anj_email_marketing.listing', {
#             'root': '/anj_email_marketing/anj_email_marketing',
#             'objects': http.request.env['anj_email_marketing.anj_email_marketing'].search([]),
#         })

#     @http.route('/anj_email_marketing/anj_email_marketing/objects/<model("anj_email_marketing.anj_email_marketing"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('anj_email_marketing.object', {
#             'object': obj
#         })
