# -*- coding: utf-8 -*-
# from odoo import http


# class AnjSubscription(http.Controller):
#     @http.route('/anj_subscription/anj_subscription/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/anj_subscription/anj_subscription/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('anj_subscription.listing', {
#             'root': '/anj_subscription/anj_subscription',
#             'objects': http.request.env['anj_subscription.anj_subscription'].search([]),
#         })

#     @http.route('/anj_subscription/anj_subscription/objects/<model("anj_subscription.anj_subscription"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('anj_subscription.object', {
#             'object': obj
#         })
