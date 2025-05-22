# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Depot(models.Model):
    _name = 'dps.depot'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Dépôt'

    montant = fields.Float(string="Montant", required=True)
    type_compte = fields.Selection([
        ('mudci', 'Contribution au budget de la mudci'),
        ('AV', 'Assurance Vie'),
        ('AS', 'Assurance Santé'),
        ('FDS', 'Fonds De Solidarité'),
        ('SFE', 'SFE'),
        ('RETRAITE', 'Cotisation Mudci Rétraite'),
    ], string="Type de Compte", required=True)

    # @api.model
    # def create(self, vals):
    #     record = super().create(vals)
    #     self._update_compte(record)
    #     return record
    #
    # def write(self, vals):
    #     res = super().write(vals)
    #     for record in self:
    #         self._update_compte(record)
    #     return res
    #
    # def unlink(self):
    #     comptes = self.mapped('type_compte')
    #     res = super().unlink()
    #     for type_compte in comptes:
    #         self._update_compte_by_type(type_compte)
    #     return res
    #
    # def _update_compte(self, record):
    #     """ Met à jour le compte correspondant au type de compte """
    #     compte = self.env['dps_comptes'].search([('type_compte', '=', record.type_compte)], limit=1)
    #     if compte:
    #         compte._compute_solde()
    #
    # def _update_compte_by_type(self, type_compte):
    #     """ Met à jour un compte en fonction du type de compte """
    #     compte = self.env['dps_comptes'].search([('type_compte', '=', type_compte)], limit=1)
    #     if compte:
    #         compte._compute_solde()