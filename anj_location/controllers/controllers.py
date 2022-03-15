# -*- coding: utf-8 -*-
# from odoo import http


# class AnjLocation(http.Controller):
#     @http.route('/anj_location/anj_location/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/anj_location/anj_location/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('anj_location.listing', {
#             'root': '/anj_location/anj_location',
#             'objects': http.request.env['anj_location.anj_location'].search([]),
#         })

#     @http.route('/anj_location/anj_location/objects/<model("anj_location.anj_location"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('anj_location.object', {
#             'object': obj
#         })
