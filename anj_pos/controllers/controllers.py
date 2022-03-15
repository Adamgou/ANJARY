# -*- coding: utf-8 -*-
# from odoo import http


# class AnjPos(http.Controller):
#     @http.route('/anj_pos/anj_pos/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/anj_pos/anj_pos/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('anj_pos.listing', {
#             'root': '/anj_pos/anj_pos',
#             'objects': http.request.env['anj_pos.anj_pos'].search([]),
#         })

#     @http.route('/anj_pos/anj_pos/objects/<model("anj_pos.anj_pos"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('anj_pos.object', {
#             'object': obj
#         })
