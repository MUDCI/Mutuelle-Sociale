# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TypePrestations(models.Model):
    _name = 'dps_type_prestations'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "id desc"
    _description = 'Type de prestation'
    _rec_name = 'typ_prest'

    # name = fields.Char("Type de prestation")
    # code = fields.Char("Code")
    # activate= fields.Boolean("Activation")
    # date_type = fields.Datetime("Date")
    cod_typ_prest = fields.Char("Code Prestation")
    typ_prest = fields.Char("Type Prestation")
    mont_prest = fields.Float("Montant Prestation")
    activate = fields.Boolean("Activation")
    date_type = fields.Datetime("Date")
    dps_prestat = fields.One2many('dps_prestation_mutualiste','dps_typprest',string='Prestation Mutualiste')
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

