# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api
from datetime import datetime


class DpsPrets(models.Model):
    _name = 'dps.prets'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Demande de Prêt'
    _rec_name = 'adherent_id'

    adherent_id = fields.Many2one('dps_mutualiste', string='Adhérent')
    adherent_name = fields.Char(string='Nom Adhérent', readonly=True, related='adherent_id.surname_mut', store=True)
    mobile = fields.Char(string='N° Mobile', readonly=True, related='adherent_id.mob_mut', store=True)
    adherent_prenoms = fields.Char(string='Prénoms Adhérent', readonly=True, related='adherent_id.lastname_mut', store=True)
    phone = fields.Char(string='N° Téléphone', readonly=True, related='adherent_id.tel_mut', store=True)
    matricule = fields.Char(string='Matricule', readonly=True, related='adherent_id.Cde_Mat', store=True)
    datenaissance = fields.Date(string='Née le', readonly=True, related='adherent_id.datnaiss_mut', store=True)
    photo = fields.Binary(string='Photo', readonly=True, related='adherent_id.image', store=True)

    pret_number = fields.Char(string='N° Dossier', readonly=True, copy=False, default="New")
    type_pret_ids = fields.Many2one('dps_type_prets', string='Type de Prêt')
    libelle_typ_pret = fields.Char(string='Libelle Pret', related='type_pret_ids.lib_typ_pret', store=True,
                                         invisible="1")
    # pret_type = fields.Selection([('FDS', 'FDS'), ('Autre', 'Autre')], string='Type de prêt')
    amount_requested = fields.Float(string='Montant sollicité')
    pret_reason = fields.Selection([('Scolarité', 'Scolarité'),
                                            ('Problèmes individuels', 'Problèmes individuels'),
                                            ('Problèmes familiaux', 'Problèmes familiaux'),
                                            ('Soins medicaux', 'Soins medicaux'),
                                            ('Autre', 'Autre')], string='Motif prêt')
    pret_date = fields.Date(string='Date de demande')
    description = fields.Text(string='Description')
    caisse_id = fields.Many2one('dps.caisse', string='Caisse')

    nom_prenoms = fields.Char(string="Nom et Prénoms", compute="_compute_name_display", store=True)
    adherent_income = fields.Float(string='Revenus adhérent', related='dps_revenu_pret.montantrevenu', store=False)
    adherent_angagement = fields.Float(string='Engagement adhérent', related='dps_engagement_mut.montant_engager', store=False)
    quotite = fields.Float(string='Quotité cessible', compute='_compute_quotite', store=False)

    # dps_revenu_pret = fields.One2many('dps_revenu', 'revenu_mut', string="Revenue Mutualiste", invisible=True)
    dps_revenu_pret = fields.One2many('dps_revenu', compute='_compute_revenus_doc_engage', string="Revenus", store=False)
    # dps_docs_mut = fields.One2many('dps.docs.mutualiste', compute='_compute_revenus_doc_engage', string="Documents Du Mutualiste")
    dps_docs_pret = fields.One2many('dps.docs.prets', 'documents_pret', string="Documents")
    dps_engagement_mut = fields.One2many('dps.engagements.mutualiste', compute='_compute_revenus_doc_engage', string="Engagement Mutualiste")

    fees_type = fields.Char(string='Type Frais')
    fees_amount = fields.Float(string='Montant', compute='_onchange_calcul_frais', store=True)
    dat_paiement = fields.Date(string='Date de paiement', default=fields.Datetime.now, invisible="1")

    start_date = fields.Date(string='Date début échéance')
    periodicity = fields.Selection([('monthly', 'Mensuel'), ('quarterly', 'Trimestriel')], string='Périodicité')
    installments = fields.Integer(string='Nombre échéance')
    amortization_lines = fields.One2many('dps.amortissement', 'pret_id', string='Tableau amortissement')

    status = fields.Selection([("creation", "En création"),
                               ("enregistrer", "Enregistrer"),
                               ("etudecs", "Approbation CS"),
                               ("etudecd", "Approbation CD"),
                               ("etudede", "Approbation DE"),
                               ("valider", "Valider"),
                               ("rejeter", "Réjéter"),
                               ("payer", "Payer"),
                               ("remboussement", "En cours de Remboussement"),
                               ("solder", "Solder"),
                               ], default="creation")

    # workfloar de validation
    def compute_inscription(self):
        self.status = 'enregistrer'

    def compute_etudecs(self):
        self.status = 'etudecs'

    def compute_etudecd(self):
        self.status = 'etudecd'

    def compute_etudede(self):
        self.status = 'etudede'

    def compute_valider(self):
        self.status = 'valider'

    def compute_rejeter(self):
        self.status = 'rejeter'

    def compute_payer(self):
        self.status = 'payer'

        self.ensure_one()  # S'assurer qu'on travaille sur un seul enregistrement

        vals = {
            'pret_number': self.pret_number,
            'amount_requested': self.amount_requested,
            'adherent_name': self.adherent_name,
            'adherent_prenoms': self.adherent_prenoms,
            'matricule': self.matricule,
            'status': self.status,
            'dat_paiement': self.dat_paiement,
            'libelle_typ_pret': self.libelle_typ_pret,
            'prets_id': self.id,
            # Ajouter tous les champs nécessaires depuis self
        }
        # Vérifier si numéro pret à enregistrer n'existe pas dans le module caisse avant de l'enregistrer
        numeroprestation = self.env['dps.caisse'].search([
            ('numdossier', '=', self.pret_number)
            # ('amortization_lines', '=', self.amortization_lines)
        ], limit=1)

        if numeroprestation:
            # Mise à jour du montant existant (ajout du nouveau montant)
            numeroprestation.write({
                'mtt_enreg': numeroprestation.mtt_enreg + self.amount_requested,
                'dat_flux': numeroprestation.dat_flux + self.dat_paiement
            })
        else:
            # Création d'un nouvel enregistrement si inexistant

            self.env['dps.caisse'].create({
                'numdossier': self.pret_number,
                'mtt_enreg': self.amount_requested,
                'nom_mut_d': self.adherent_name,
                'prenom_mut_d': self.adherent_prenoms,
                'cde_adh_mat_caisse': self.matricule,
                'status': self.status,
                'dat_flux': self.dat_paiement,
                'type_pret_caisse': self.libelle_typ_pret,
                'prets_id': self.id,
                # Ajoutez ici les autres champs obligatoires
            })

            cotisation = super(DpsPrets, self).create(vals)

            # Vérifier si une entrée pour ce type de cotisation existe déjà du retrait
            pret_type = self.type_pret_ids
            type_label = 'FDS'  # Valeur par défaut

            if pret_type and pret_type[0].name == 'SFE':
                type_label = 'SFE'

            entree = self.env['dps.retrait'].search([
                ('type_compte', '=', type_label)
            ], limit=1)

            if entree:
                # Mise à jour du montant existant (ajout du nouveau montant)
                entree.write({
                    'montant': entree.montant + cotisation.amount_requested
                })
            else:
                # Création d'une nouvelle entrée
                self.env['dps.depot'].create({
                    'type_compte': type_label,
                    'montant': cotisation.amount_requested
                })

                # Vérifier si une entrée pour ce type de cotisation existe déjà au niveau du compte
                entreecompte = self.env['dps_comptes'].search([
                    ('type_compte', '=', type_label)
                ], limit=1)

                if entreecompte:
                    # Mise à jour du montant existant (ajout du nouveau montant)
                    entreecompte.write({
                        'total_depot': entreecompte.total_depot + cotisation.amount_requested
                    })
                else:
                    # Création d'une nouvelle entrée
                    self.env['dps_comptes'].create({
                        'type_compte': type_label,
                        'total_depot': cotisation.amount_requested
                    })

                return cotisation

    def compute_remboussement(self):
        self.status = 'remboussement'

    def compute_solder(self):
        self.status = 'solder'

    def compute_creation(self):
        self.status = 'creation'

    # Calcule de quotité cessible
    @api.depends('adherent_income', 'amount_requested', 'adherent_angagement', 'type_pret_ids')
    def _compute_quotite(self):
        for record in self:
            base = record.adherent_income - record.adherent_angagement
            if record.type_pret_ids.cod_typ_pret == 'SFE':
                record.quotite = (base * 2/3) if record.adherent_income else 0
            else:
                record.quotite = (base / 2) if record.adherent_income else 0
                # record.quotite = (record.amount_requested * 0.95) if record.adherent_income else 0


    # def compute_quotite(self):
    #     for record in self:
    #         record.quotite = (record.amount_requested * 0.95) if record.adherent_income else 0

    # Creation de numero de dossier
    @api.model
    def create(self, vals):
        if vals.get("pret_number", "New") == "New":
            current_year = datetime.now().year
            last_record = self.sudo().search([], order="id desc", limit=1)
            next_number = last_record.id + 1 if last_record else 1
            vals["pret_number"] = f"DPS-{current_year}-{next_number:04d}"  # Ex: DPS-2025-0001
        return super(DpsPrets, self).create(vals)

    # Concatenation de nom et prénoms
    @api.depends('adherent_name', 'adherent_prenoms')
    def _compute_name_display(self):
        for record in self:
            record.nom_prenoms = f"{record.adherent_name or ''} {record.adherent_prenoms or ''}".strip()

    # Recuperation de revenu,document,et engagement adherents
    @api.depends('adherent_id')
    def _compute_revenus_doc_engage(self):
        for rec in self:
            rec.dps_revenu_pret = rec.adherent_id.dps_revenu_mut
            # rec.dps_docs_mut = rec.adherent_id.dps_docs_mut
            rec.dps_engagement_mut = rec.adherent_id.dps_engagement_mut

    # Calcul de frais de dossier
    # Calcul de frais de dossier
    @api.onchange('type_pret_ids', 'amount_requested')
    def _onchange_calcul_frais(self):
        if self.type_pret_ids and self.amount_requested:
            frais = self.env['dps.frais'].search([
                ('type_pret_ids', '=', self.type_pret_ids.id),
                ('montant_min', '<=', self.amount_requested),
                ('montant_max', '>=', self.amount_requested)
            ], limit=1)

            if frais:
                self.fees_amount = frais.montant_frais
            else:
                self.fees_amount = 0


    # Calcule de l'amortissement
    def generate_amortissement(self):
        for record in self:
            record.amortization_lines.unlink()
            amount_per_installment = record.amount_requested / record.installments if record.installments else 0
            date = record.start_date
            delta = relativedelta(months=1) if record.periodicity == 'monthly' else relativedelta(months=3)

            for i in range(1, record.installments + 1):
                self.env['dps.amortissement'].create({
                    'pret_id': record.id,
                    'installment_number': i,
                    'due_date': date,
                    'installment_amount': amount_per_installment,
                })
                date += delta

    # Remboussement a la caisse
    rembourssement_count = fields.Integer(string="Facture a remboursser", compute="_get_rembourssement_count")

    def _get_rembourssement_count(self):
        self.rembourssement_count = len(self.amortization_lines)

    def rembourssement_list(self):
        return {
            'name': 'Facture a rembourssée',
            'domain': [('pret_id', '=', self.id)],
            'res_model': 'dps.amortissement',
            'view_id': True,
            # 'view_id': self.env.ref('rembourssement_list').id,
            'view_mode': 'tree,form',
            'context': {'default_amortization_lines': self.id},
            'type': 'dps_prets_action_window',
            # 'type': 'ir.actions.act_window',
        }

# Modèl amortissement
class Amortissement(models.Model):
    _name = 'dps.amortissement'
    _description = 'Amortissement du prêt'

    pret_id = fields.Many2one('dps.prets', string='Demande de prêt')
    installment_number = fields.Integer(string='N° Échéance')
    due_date = fields.Date(string='Date échéance')
    installment_amount = fields.Float(string='Montant échéance')
    etat_paiement = fields.Boolean(string='Etat de paiement')
    date_paiement = fields.Date(string='Date de paiement')


# La classe des documents du mutualiste
class DpsDocsPret(models.Model):
    _name = 'dps.docs.prets'
    _order = "id desc"
    _description = 'Documents Prêts'

    dat_recept = fields.Date("Date De Réception")
    ref_docs = fields.Char("Référence Du Document")
    typ_docs = fields.Selection([("CNI","Carte National Identité (CNI)"),
                                 ("AN","Acte / Extrait de naissance"),
                                 ("PJC","Pièces justificatives du crédit"),
                                 ("BP","Bulletin de prime"),
                                 ("CM","Carte MUDCI"),
                                 ("CMU","Carte CMU"),
                                 ("DP","Demande de prêt"),
                                 ("BS","Bulletin de salaire")], string="Type De Document")
    dat_etablir = fields.Datetime("Date établissement")
    dat_valid_docs = fields.Date("Date De Validité")
    image_docs = fields.Binary("Documents")
    active_docs = fields.Char("Activation", default="Oui")
    documents_pret = fields.Many2one('dps.prets', string="Documents Mutualiste")