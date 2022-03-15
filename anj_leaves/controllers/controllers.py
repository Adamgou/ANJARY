# -*- coding: utf-8 -*-
# from odoo import http


# class AnjLeaves(http.Controller):
#     @http.route('/anj_leaves/anj_leaves/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/anj_leaves/anj_leaves/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('anj_leaves.listing', {
#             'root': '/anj_leaves/anj_leaves',
#             'objects': http.request.env['anj_leaves.anj_leaves'].search([]),
#         })

#     @http.route('/anj_leaves/anj_leaves/objects/<model("anj_leaves.anj_leaves"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('anj_leaves.object', {
#             'object': obj
#         })
