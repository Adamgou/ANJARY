# -*- coding: utf-8 -*-
# from odoo import http


# class AnjDocument(http.Controller):
#     @http.route('/anj_document/anj_document/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/anj_document/anj_document/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('anj_document.listing', {
#             'root': '/anj_document/anj_document',
#             'objects': http.request.env['anj_document.anj_document'].search([]),
#         })

#     @http.route('/anj_document/anj_document/objects/<model("anj_document.anj_document"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('anj_document.object', {
#             'object': obj
#         })
