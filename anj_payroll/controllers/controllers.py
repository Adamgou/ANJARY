# -*- coding: utf-8 -*-
# from odoo import http


# class AnjPayroll(http.Controller):
#     @http.route('/anj_payroll/anj_payroll/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/anj_payroll/anj_payroll/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('anj_payroll.listing', {
#             'root': '/anj_payroll/anj_payroll',
#             'objects': http.request.env['anj_payroll.anj_payroll'].search([]),
#         })

#     @http.route('/anj_payroll/anj_payroll/objects/<model("anj_payroll.anj_payroll"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('anj_payroll.object', {
#             'object': obj
#         })
