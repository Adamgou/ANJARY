# -*- coding: utf-8 -*-
# from odoo import http


# class AnjSale(http.Controller):
#     @http.route('/anj_sale/anj_sale/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/anj_sale/anj_sale/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('anj_sale.listing', {
#             'root': '/anj_sale/anj_sale',
#             'objects': http.request.env['anj_sale.anj_sale'].search([]),
#         })

#     @http.route('/anj_sale/anj_sale/objects/<model("anj_sale.anj_sale"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('anj_sale.object', {
#             'object': obj
#         })
