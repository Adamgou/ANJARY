# -*- coding: utf-8 -*-
# from odoo import http


# class AnjBase(http.Controller):
#     @http.route('/anj_base/anj_base/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/anj_base/anj_base/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('anj_base.listing', {
#             'root': '/anj_base/anj_base',
#             'objects': http.request.env['anj_base.anj_base'].search([]),
#         })

#     @http.route('/anj_base/anj_base/objects/<model("anj_base.anj_base"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('anj_base.object', {
#             'object': obj
#         })
