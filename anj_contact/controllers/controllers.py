# -*- coding: utf-8 -*-
# from odoo import http


# class AnjContact(http.Controller):
#     @http.route('/anj_contact/anj_contact/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/anj_contact/anj_contact/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('anj_contact.listing', {
#             'root': '/anj_contact/anj_contact',
#             'objects': http.request.env['anj_contact.anj_contact'].search([]),
#         })

#     @http.route('/anj_contact/anj_contact/objects/<model("anj_contact.anj_contact"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('anj_contact.object', {
#             'object': obj
#         })
