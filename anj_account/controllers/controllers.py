# -*- coding: utf-8 -*-
# from odoo import http


# class AnjAccount(http.Controller):
#     @http.route('/anj_account/anj_account/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/anj_account/anj_account/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('anj_account.listing', {
#             'root': '/anj_account/anj_account',
#             'objects': http.request.env['anj_account.anj_account'].search([]),
#         })

#     @http.route('/anj_account/anj_account/objects/<model("anj_account.anj_account"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('anj_account.object', {
#             'object': obj
#         })
