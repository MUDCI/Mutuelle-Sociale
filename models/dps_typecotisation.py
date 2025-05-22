# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TypeCotisation(models.Model):
    _name = 'dps_type_cotisation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "id desc"
    _description = 'Type de cotisation'

    name = fields.Char("Type de cotisation")
    code = fields.Char("Code")
    activate= fields.Boolean("Activation")
    date_type = fields.Datetime("Date")
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

