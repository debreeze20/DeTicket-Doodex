# -*- coding: utf-8 -*-
# from odoo import http


# class Eventmanagementnew(http.Controller):
#     @http.route('/eventmanagementnew/eventmanagementnew', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/eventmanagementnew/eventmanagementnew/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('eventmanagementnew.listing', {
#             'root': '/eventmanagementnew/eventmanagementnew',
#             'objects': http.request.env['eventmanagementnew.eventmanagementnew'].search([]),
#         })

#     @http.route('/eventmanagementnew/eventmanagementnew/objects/<model("eventmanagementnew.eventmanagementnew"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('eventmanagementnew.object', {
#             'object': obj
#         })
