# -*- coding: utf-8 -*-
# from odoo import http


# class HhSalesInherit(http.Controller):
#     @http.route('/hh_sales_inherit/hh_sales_inherit', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hh_sales_inherit/hh_sales_inherit/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hh_sales_inherit.listing', {
#             'root': '/hh_sales_inherit/hh_sales_inherit',
#             'objects': http.request.env['hh_sales_inherit.hh_sales_inherit'].search([]),
#         })

#     @http.route('/hh_sales_inherit/hh_sales_inherit/objects/<model("hh_sales_inherit.hh_sales_inherit"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hh_sales_inherit.object', {
#             'object': obj
#         })
