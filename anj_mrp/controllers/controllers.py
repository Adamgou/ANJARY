# -*- coding: utf-8 -*-
# from odoo import http


# class AnjMrp(http.Controller):
#     @http.route('/anj_mrp/anj_mrp', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/anj_mrp/anj_mrp/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('anj_mrp.listing', {
#             'root': '/anj_mrp/anj_mrp',
#             'objects': http.request.env['anj_mrp.anj_mrp'].search([]),
#         })

#     @http.route('/anj_mrp/anj_mrp/objects/<model("anj_mrp.anj_mrp"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('anj_mrp.object', {
#             'object': obj
#         })
