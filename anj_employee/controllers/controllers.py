# -*- coding: utf-8 -*-
# from odoo import http


# class AnjEmployee(http.Controller):
#     @http.route('/anj_employee/anj_employee/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/anj_employee/anj_employee/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('anj_employee.listing', {
#             'root': '/anj_employee/anj_employee',
#             'objects': http.request.env['anj_employee.anj_employee'].search([]),
#         })

#     @http.route('/anj_employee/anj_employee/objects/<model("anj_employee.anj_employee"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('anj_employee.object', {
#             'object': obj
#         })
