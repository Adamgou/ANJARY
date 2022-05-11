# -*- coding: utf-8 -*-
# from odoo import http


# class AnjCalendar(http.Controller):
#     @http.route('/anj_calendar/anj_calendar', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/anj_calendar/anj_calendar/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('anj_calendar.listing', {
#             'root': '/anj_calendar/anj_calendar',
#             'objects': http.request.env['anj_calendar.anj_calendar'].search([]),
#         })

#     @http.route('/anj_calendar/anj_calendar/objects/<model("anj_calendar.anj_calendar"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('anj_calendar.object', {
#             'object': obj
#         })
