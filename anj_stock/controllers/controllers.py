# -*- coding: utf-8 -*-
# from odoo import http


# class AnjStock(http.Controller):
#     @http.route('/anj_stock/anj_stock/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/anj_stock/anj_stock/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('anj_stock.listing', {
#             'root': '/anj_stock/anj_stock',
#             'objects': http.request.env['anj_stock.anj_stock'].search([]),
#         })

#     @http.route('/anj_stock/anj_stock/objects/<model("anj_stock.anj_stock"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('anj_stock.object', {
#             'object': obj
#         })
