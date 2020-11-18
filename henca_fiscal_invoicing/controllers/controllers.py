# -*- coding: utf-8 -*-
# from odoo import http


# class HencaFiscal(http.Controller):
#     @http.route('/henca_fiscal/henca_fiscal/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/henca_fiscal/henca_fiscal/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('henca_fiscal.listing', {
#             'root': '/henca_fiscal/henca_fiscal',
#             'objects': http.request.env['henca_fiscal.henca_fiscal'].search([]),
#         })

#     @http.route('/henca_fiscal/henca_fiscal/objects/<model("henca_fiscal.henca_fiscal"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('henca_fiscal.object', {
#             'object': obj
#         })
