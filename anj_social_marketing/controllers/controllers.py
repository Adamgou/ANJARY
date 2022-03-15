# -*- coding: utf-8 -*-
# from odoo import http


# class AnjSocialMarketing(http.Controller):
#     @http.route('/anj_social_marketing/anj_social_marketing/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/anj_social_marketing/anj_social_marketing/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('anj_social_marketing.listing', {
#             'root': '/anj_social_marketing/anj_social_marketing',
#             'objects': http.request.env['anj_social_marketing.anj_social_marketing'].search([]),
#         })

#     @http.route('/anj_social_marketing/anj_social_marketing/objects/<model("anj_social_marketing.anj_social_marketing"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('anj_social_marketing.object', {
#             'object': obj
#         })
