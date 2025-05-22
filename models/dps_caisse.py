# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api
from datetime import datetime


class DpsPrets(models.Model):
    _name = 'dps.caisse'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Rembourssement des prets'
    # _rec_name = 'adherent_id'

    # name = fields.Char(string='Nom Caisse')
    # prets_ids = fields.One2many('dps.prets', 'id',string='Prêts liés')
    # prets_ids = fields.One2many('dps.prets', 'id',string='Prêts liés', compute='_compute_pret_ids', store=False)
    # numdossier = fields.Char(string='N° Dossier', readonly=True, related='prets_ids.pret_number', store=True)

    numdossier = fields.Char(string='N° Dossier', readonly=True, store=True)
    mtt_enreg = fields.Float(string='Montant Payer', readonly=True)
    nom_mut_d = fields.Char(string='Nom', readonly=True)
    prenom_mut_d = fields.Char(string='Prenoms', readonly=True)
    cde_adh_mat_caisse = fields.Char(string='Matricule', readonly=True)
    dat_flux = fields.Datetime(string='Date de paiement', readonly=True, default=fields.Datetime.now)
    type_pret_caisse = fields.Char(string='Type de Prêt', readonly=True)
    prets_id = fields.Many2one('dps.prets', string='ID', readonly=True)
    # amortization_lines = fields.One2many('dps.prets', 'pret_id', string='Montant par echéance')
    echeanchier = fields.One2many('dps.amortissement', compute='_compute_amortissement', string="Montant par echéance")


    status = fields.Selection([("payer", "Payer"),
                               ("remboussement", "En cours de Remboussement"),
                               ("solder", "Solder"),
                               ], readonly=True, string="Statut")

    # Recuperation de Amortissement du prêt
    @api.depends('prets_id')
    def _compute_amortissement(self):
        for rec in self:
            rec.echeanchier = rec.prets_id.amortization_lines


    # def rembourssement_list(self):
    #     return {
    #         'name': 'Facture a rembourssée',
    #         'domain': [('pret_id', '=', self.id)],
    #         'res_model': 'dps.amortissement',
    #         'view_id': False,
    #         # 'view_id': self.env.ref('rembourssement_list').id,
    #         'view_mode': 'tree,form',
    #         'context': {'default_amortization_lines': self.id},
    #         # 'type': 'dps_prets_action_window',
    #         'type': 'ir.actions.act_window',
    #     }

    # workfloar de validation

    def compute_payer(self):
        self.status = 'payer'

    def compute_remboussement(self):
        self.status = 'remboussement'

    def compute_solder(self):
        self.status = 'solder'

    #  recuperation des prêts
    @api.depends()
    def _compute_pret_ids(self):
        for record in self:
            record.prets_ids = self.env['dps.prets'].search([
                ('status', 'in', ['payer', 'remboussement'])
            ])

# class AmortissementCaisse(models.Model):
#     _name = 'dps.amortissement.caisse'
#     _description = 'Amortissement de la Caisse'
#
#     caisse_id = fields.Many2one('dps.caisse', string='Caisse')
#     installment_number = fields.Integer(string='N° Échéance')
#     due_date = fields.Date(string='Date échéance')
#     installment_amount = fields.Float(string='Montant échéance')
#     etat_paiement = fields.Boolean(string='Etat de paiement')
#     date_paiement = fields.Date(string='Date de paiement')
