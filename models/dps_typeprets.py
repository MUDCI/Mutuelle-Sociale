# -*- coding: utf-8 -*-

from odoo import models, fields, api
# from odoo.exceptions import ValidationError

class TypePrets(models.Model):
    _name = 'dps_type_prets'
    _order = "id desc"
    _description = 'Type de prêts'
    _rec_name = 'lib_typ_pret'

    lib_typ_pret = fields.Char("Type de prêt")
    cod_typ_pret = fields.Char("Code")
    activate_typ_pret = fields.Boolean("Activation")
    date_typ_pret = fields.Datetime("Date")
    dps_frais_doc = fields.One2many('dps.frais', 'type_pret_ids', string="Frais de Dossier")



class FraisDossier(models.Model):
    _name = 'dps.frais'
    _order = 'id desc'
    _description = 'Frais de Dossier'

    montant_min = fields.Float('Montant Min')
    montant_max = fields.Float('Montant Max')
    montant_frais = fields.Float('Frais')
    type_pret_ids = fields.Many2one('dps_type_prets', string='Type de Prêt')


# class FormuleCotite(models.Model):
#     _name = 'dps.cotite'
#     _order = 'id desc'
#     _description = 'Formule de Cotité'
#
#     libelle_cotite = fields.Char('Libelle')
#     revenu_cotite = fields.Many2one('dps_revenu', string='Revenu')
#     operation_cotite = fields.Selection([('monthly', 'Mensuel'),
#                                          ('quarterly', 'Trimestriel'),
#                                          ('quarterly', 'Trimestriel'),
#                                          ], string='Operation')
#     type_pret_ids = fields.Many2one('dps_type_prets', string='Type de Prêt')