# -*- coding: utf-8 -*-
# from odoo import http


# class MutuelleSociale(http.Controller):
#     @http.route('/mutuelle_sociale/mutuelle_sociale', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mutuelle_sociale/mutuelle_sociale/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('mutuelle_sociale.listing', {
#             'root': '/mutuelle_sociale/mutuelle_sociale',
#             'objects': http.request.env['mutuelle_sociale.mutuelle_sociale'].search([]),
#         })

#     @http.route('/mutuelle_sociale/mutuelle_sociale/objects/<model("mutuelle_sociale.mutuelle_sociale"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mutuelle_sociale.object', {
#             'object': obj
#         })

