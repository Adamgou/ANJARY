# -*- coding: utf-8 -*-
# from odoo import http


# class AnjQuality(http.Controller):
#     @http.route('/anj_quality/anj_quality/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/anj_quality/anj_quality/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('anj_quality.listing', {
#             'root': '/anj_quality/anj_quality',
#             'objects': http.request.env['anj_quality.anj_quality'].search([]),
#         })

#     @http.route('/anj_quality/anj_quality/objects/<model("anj_quality.anj_quality"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('anj_quality.object', {
#             'object': obj
#         })
