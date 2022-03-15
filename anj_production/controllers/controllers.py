# -*- coding: utf-8 -*-
# from odoo import http


# class AnjProduction(http.Controller):
#     @http.route('/anj_production/anj_production/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/anj_production/anj_production/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('anj_production.listing', {
#             'root': '/anj_production/anj_production',
#             'objects': http.request.env['anj_production.anj_production'].search([]),
#         })

#     @http.route('/anj_production/anj_production/objects/<model("anj_production.anj_production"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('anj_production.object', {
#             'object': obj
#         })
