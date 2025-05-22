# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Comptes(models.Model):
    _name = 'dps_comptes'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "id desc"
    _description = 'Les Comptes'

    type_compte = fields.Selection([
        ('mudci', 'Contribution au budget de la mudci'),
        ('AV', 'Assurance Vie'),
        ('AS', 'Assurance Santé'),
        ('FDS', 'Fonds De Solidarité'),
        ('SFE', 'SFE'),
        ('RETRAITE', 'Cotisation Mudci Rétraite'),
    ], string="Type de Compte", required=True)

    total_depot = fields.Float(string="Total Dépôt", store=True)
    total_retrait = fields.Float(string="Total Retrait", store=True)
    solde = fields.Float(string="Solde", compute="_get_solde", store=True)

    @api.depends('total_depot', 'total_retrait')
    def _get_solde(self):
        for record in self:
            record.solde = record.total_depot - record.total_retrait

    # total_depot = fields.Float(string="Total Dépôt", compute="_compute_totals", store=True)
    # total_retrait = fields.Float(string="Total Retrait", compute="_compute_totals", store=True)
    # solde = fields.Float(string="Solde", compute="_compute_totals", store=True)
    #
    # @api.depends('type_compte')
    # def _compute_totals(self):
    #     for record in self:
    #         depots = self.env['dps.depot'].search([('type_compte', '=', record.type_compte)])
    #         retraits = self.env['dps.retrait'].search([('type_compte', '=', record.type_compte)])
    #         record.total_depot = sum(depots.mapped('montant'))
    #         record.total_retrait = sum(retraits.mapped('montant'))
    #         record.solde = record.total_depot - record.total_retrait
