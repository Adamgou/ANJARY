# -*- coding: utf-8 -*-
# from odoo import http


# class TnxEmployee(http.Controller):
#     @http.route('/alpha_payslip/alpha_payslip/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/alpha_payslip/alpha_payslip/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('alpha_payslip.listing', {
#             'root': '/alpha_payslip/alpha_payslip',
#             'objects': http.request.env['alpha_payslip.alpha_payslip'].search([]),
#         })

#     @http.route('/alpha_payslip/alpha_payslip/objects/<model("alpha_payslip.alpha_payslip"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('alpha_payslip.object', {
#             'object': obj
#         })
