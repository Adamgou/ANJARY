# -*- coding: utf-8 -*-
# from odoo import http


# class AnjFleet(http.Controller):
#     @http.route('/anj_fleet/anj_fleet/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/anj_fleet/anj_fleet/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('anj_fleet.listing', {
#             'root': '/anj_fleet/anj_fleet',
#             'objects': http.request.env['anj_fleet.anj_fleet'].search([]),
#         })

#     @http.route('/anj_fleet/anj_fleet/objects/<model("anj_fleet.anj_fleet"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('anj_fleet.object', {
#             'object': obj
#         })
