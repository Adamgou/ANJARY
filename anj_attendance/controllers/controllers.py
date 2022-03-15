# -*- coding: utf-8 -*-
# from odoo import http


# class AnjAttendance(http.Controller):
#     @http.route('/anj_attendance/anj_attendance/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/anj_attendance/anj_attendance/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('anj_attendance.listing', {
#             'root': '/anj_attendance/anj_attendance',
#             'objects': http.request.env['anj_attendance.anj_attendance'].search([]),
#         })

#     @http.route('/anj_attendance/anj_attendance/objects/<model("anj_attendance.anj_attendance"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('anj_attendance.object', {
#             'object': obj
#         })
