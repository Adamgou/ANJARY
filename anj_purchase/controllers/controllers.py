# -*- coding: utf-8 -*-
# from odoo import http


# class AnjPurchase(http.Controller):
#     @http.route('/anj_purchase/anj_purchase/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/anj_purchase/anj_purchase/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('anj_purchase.listing', {
#             'root': '/anj_purchase/anj_purchase',
#             'objects': http.request.env['anj_purchase.anj_purchase'].search([]),
#         })

#     @http.route('/anj_purchase/anj_purchase/objects/<model("anj_purchase.anj_purchase"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('anj_purchase.object', {
#             'object': obj
#         })
