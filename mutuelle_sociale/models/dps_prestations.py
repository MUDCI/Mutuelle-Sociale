# -*- coding: utf-8 -*-
from email.policy import default
from symtable import Class

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime

class DpsPrestation(models.Model):
    _name = 'dps_prestation_mutualiste'
    _order = "id desc"
    _description = 'Prestation Mutualiste'
    _inherit = ['dps_mutualiste','dps_type_prestations']
    # _rec_name = 'adh_id'
    _rec_names_search = ['dps_typprest', 'adh_id']

    # Champs sous onglet - Adhérent

    adh_id = fields.Many2one('dps_mutualiste', string=' Recherche Adhérent')
    cde_id_mut = fields.Char(string='Code ID', readonly=True, related='adh_id.Cde_ID', store=True)
    cde_adh_mat = fields.Char(string='Matricule', readonly=True, related='adh_id.Cde_Mat', store=True)
    adh_nm = fields.Char(string='Nom', readonly=True, related='adh_id.surname_mut', store=True)
    adh_prnms = fields.Char(string='Prenoms', readonly=True, related='adh_id.lastname_mut', store=True)
    adh_datenaiss = fields.Date(string='Date De Naissance', readonly=True, related='adh_id.datnaiss_mut', store=True)
    adh_stat = fields.Char(string='Status', readonly=True, related='adh_id.statut_mut', store=True)
    adh_sex = fields.Selection(string='Genre', readonly=True, related='adh_id.genr_mut', store=True)
    adh_photo = fields.Binary(string='', related='adh_id.image', store=True)

    # Champs sous onglets - Prestation
    prest_auto_increment = fields.Char(string='N° Prestation', readonly=True, copy=False, default="New")

    dps_typprest = fields.Many2one('dps_type_prestations', string='Type de Prestation')
    montant_prestation = fields.Float(string='Montant Prestation', related='dps_typprest.mont_prest', store=True)
    libelle_typ_prestation = fields.Char(string='Libelle Prestation', related='dps_typprest.typ_prest', store=True,
                                         invisible="1")
    dat_demande = fields.Date("Date De La Demande")
    dat_enlevemnt = fields.Date("Date Evènement")
    dat_paiement = fields.Date(string='Date de paiement', default=fields.Datetime.now, invisible="1")
    lieu_enlevemnt = fields.Selection([("abidjan", "ABIDJAN"),
                                                ("abengourou", "ABENGOUROU"),
                                                ("aboisso", "ABOISSO"),
                                                ("aboisso", "ABOISSO"),
                                                ("aboisso", "ABOISSO"),
                                                ("adiake", "ADIAKE"),
                                                ("adzopé", "ADZOPE"),
                                                ("agboville", "AGBOVILLE"),
                                                ("agnibilékro", "AGNIBILEKRO"),
                                                ("akoupé", "AKOUPE"),
                                                ("anyama", "ANYAMA"),
                                                ("arrah", "ARRAH"),
                                                ("assuefry", "ASSUEFRY"),
                                                ("ayamé", "AYAME"),
                                                ("azaguié", "AZAGUIE"),
                                                ("anoumaba", "ANOUMABA"),
                                                ("bangolo", "BANGOLO"),
                                                ("becedi", "BECEDI"),
                                                ("béoumi", "BEOUMI"),
                                                ("bia", "BIA"),
                                                ("bimbresso", "BIMBRESSO"),
                                                ("bingerville", "BINGERVILLE"),
                                                ("bocanda", "BOCANDA"),
                                                ("bondoukou", "BONDOUKOU"),
                                                ("bongo", "BONGO"),
                                                ("bongouanou", "BONGOUANOU"),
                                                ("bonoua", "BONOUA"),
                                                ("botro", "BOTRO"),
                                                ("bouaflé", "BOUAFLÉ"),
                                                ("bouaké", "BOUAKE"),
                                                ("bouna", "BOUNA"),
                                                ("boundiali", "BOUNDIALI"),
                                                ("dabakala", "DABAKALA"),
                                                ("dabou", "DABOU"),
                                                ("daloa", "DALOA"),
                                                ("danané", "DANANE"),
                                                ("daoukro", "DAOUKRO"),
                                                ("didievi", "DIDIEVI"),
                                                ("dimbokro", "DIMBOKRO"),
                                                ("divo", "DIVO"),
                                                ("djébonoua", "DJEBONOUA"),
                                                ("duékoué", "DUEKOUE"),
                                                ("ferkessédougou", "FERKESSEDOUGOU"),
                                                ("fresco", "FRESCO"),
                                                ("gagnoa", "GAGNOA"),
                                                ("gonaté", "GONATE"),
                                                ("grand-bassam", "GRAND-BASSAM"),
                                                ("grand-béréby", "GRAND-BEREBY"),
                                                ("grand-lahou", "GRAND-LAHOU"),
                                                ("guéyo", "GUEYO"),
                                                ("guessabo", "GUESSABO"),
                                                ("guiglo", "GUIGLO"),
                                                ("guitry", "GUITRY"),
                                                ("issia", "ISSIA"),
                                                ("kani", "KANI"),
                                                ("katiola", "KATIOLA"),
                                                ("kokumbo", "KOKUMBO"),
                                                ("kungasso", "KUNGASSO"),
                                                ("korhogo", "KORHOGO"),
                                                ("kotobi", "КОТОВІ"),
                                                ("koun-fao", "KOUN-FAO"),
                                                ("lakota", "LAKOTA"),
                                                ("logoualé", "LOGOUALE"),
                                                ("m'bahiakro", "M'BAHIAKRO"),
                                                ("man", "MAN"),
                                                ("mankono", "MANKONO"),
                                                ("n’douci", "N'DOUCI"),
                                                ("niakara", "NIAKARA"),
                                                ("niellé", "NIELLE"),
                                                ("odienné", "ODIENNE"),
                                                ("ouangolodougou", "OUANGOLO"),
                                                ("ouellé", "OUELLE"),
                                                ("oumé", "OUME"),
                                                ("pakobo", "РАКОВО"),
                                                ("sakassou", "SAKASSOU"),
                                                ("san-pédro", "SAN-PEDRO"),
                                                ("sassandra", "SASSANDRA"),
                                                ("séguéla", "SEGUELA"),
                                                ("sinfra", "SINFRA"),
                                                ("soubré", "SOUBRE"),
                                                ("tabou", "TABOU"),
                                                ("tafira", "TAFIRE"),
                                                ("tanda", "TANDA"),
                                                ("taï", "TAI"),
                                                ("tiassalé", "TIASSALE"),
                                                ("tiébissou", "TIEBISSOU"),
                                                ("tiémélékro", "TIEMELEKRO"),
                                                ("tingréla", "TINGRELA"),
                                                ("tortiya", "TORTIYA"),
                                                ("touba", "TOUBA"),
                                                ("toulépleu", "TOULEPLEU"),
                                                ("toumodi", "TOUMODI"),
                                                ("toupah", "TOUPAH"),
                                                ("vavoua", "VAVOUA"),
                                                ("yamoussoukro", "YAMOUSSOUKRO"),
                                                ("yokoboué", "YOKOBOUE"),
                                                ("zuenoula", "ZUENOULA")],string="Lieu Evènement")


    #One2Many Intervenants
    dps_intervenant = fields.One2many('dps.intervenant.mutualiste', 'intervants_dps', string="Intervenant")

    typ_prestat = fields.Char(string='Type Intervention', readonly=True, related='dps_typprest.typ_prest', store=True)

    #One2Many Documents Prestations
    dps_docs_mut_prest = fields.One2many('dps.documents.prestations', 'documents_mut_prest', string="Document Prestation")

    # Worflow
    statut_prestation = fields.Selection([("encreation","En création"),
                                          ("enregistrer","Enregistrer"),
                                          ("rejeter","Suspendue"),
                                          ("appro_cs","Approbation CS"),
                                          ("appro_cd","Approbation CD"),
                                          ("appro_de","Approbation DE"),
                                          ("valider","Valider"),
                                          ("payer","Payer")], default="encreation", string="Statut Prestation")

    @api.model
    def create(self, vals):
        if vals.get("pret_number", "New") == "New":
            current_year = datetime.now().year
            last_record = self.search([], order="id desc", limit=1)
            next_number = last_record.id + 1 if last_record else 1
            vals["prest_auto_increment"] = f"DPS_PREST-{current_year}-{next_number:04d}"  # Ex: DPS_PREST-2025-0001
        return super(DpsPrestation, self).create(vals)

    # Fonction workflow - En Création
    def compute_prestationssocial_encreat(self):
        self.statut_prestation ='encreation'

    # Fonction workflow - Enregistrer
    def compute_prestationssocial(self):
        self.statut_prestation ='enregistrer'

    # Fonction workflow - Approbation CS
    def compute_prestationssocial_cs(self):
        self.statut_prestation ='appro_cs'

    # Fonction workflow - Approbation CD
    def compute_prestationssocial_cd(self):
        self.statut_prestation ='appro_cd'

    # Fonction workflow - Approbation DE
    def compute_prestationssocial_de(self):
        self.statut_prestation ='appro_de'

    # Fonction workflow - Approbation DE
    def compute_prestationssocial_appro_de(self):
        self.statut_prestation ='valider'

    # Fonction workflow - Valider
    def compute_prestationssocial_valide(self):
        self.statut_prestation ='payer'

        self.ensure_one()  # S'assurer qu'on travaille sur un seul enregistrement

        vals = {
            'prest_auto_increment': self.prest_auto_increment,
            'montant_prestation': self.montant_prestation,
            'adh_nm': self.adh_nm,
            'adh_prnms': self.adh_prnms,
            'cde_adh_mat': self.cde_adh_mat,
            'statut_prestation': self.statut_prestation,
            'dat_paiement': self.dat_paiement,
            'libelle_typ_prestation': self.libelle_typ_prestation,
            # Ajouter tous les champs nécessaires depuis self
        }
        # Vérifier si numéro prestation à enregistrer n'existe pas dans le module caisse avant de l'enregistrer
        numeroprestation = self.env['dps.caisse.prestation'].search([
            ('prest_auto_increment_caisse', '=', self.prest_auto_increment)
        ], limit=1)

        if numeroprestation:
            # Mise à jour du montant existant (ajout du nouveau montant)
            numeroprestation.write({
                'mtt_enreg': numeroprestation.mtt_enreg + self.montant_prestation,
                'dat_flux': numeroprestation.dat_flux + self.dat_paiement
            })
        else:
            # Création d'un nouvel enregistrement si inexistant

            self.env['dps.caisse.prestation'].create({
                'prest_auto_increment_caisse': self.prest_auto_increment,
                'mtt_enreg': self.montant_prestation,
                'nom_mut_d': self.adh_nm,
                'prenom_mut_d': self.adh_prnms,
                'cde_adh_mat_caisse': self.cde_adh_mat,
                'statut_prestation_caisse': self.statut_prestation,
                'dat_flux': self.dat_paiement,
                'type_prestation_caisse': self.libelle_typ_prestation,
                # Ajoutez ici les autres champs obligatoires
            })

        # cotisation = super(DpsPrestation, self).create(vals)

        # Vérifier si une entrée pour ce type de cotisation existe déjà du retrait
        entree = self.env['dps.retrait'].search([
            ('type_compte', '=', 'AV')
        ], limit=1)

        if entree:
            # Mise à jour du montant existant (ajout du nouveau montant)
            entree.write({
                'montant': entree.montant + self.montant_prestation
            })
        else:
            # Création d'une nouvelle entrée
            self.env['dps.retrait'].create({
                'type_compte': 'AV',
                'montant': self.montant_prestation
            })

        # Vérifier si une entrée pour ce type de cotisation existe déjà au niveau du compte
        entreecompte = self.env['dps_comptes'].search([
            ('type_compte', '=', 'AV')
        ], limit=1)

        if entreecompte:
            # Mise à jour du montant existant (ajout du nouveau montant)
            entreecompte.write({
                'total_retrait': entreecompte.total_retrait + self.montant_prestation
            })
        else:
            # Création d'une nouvelle entrée
            self.env['dps_comptes'].create({
                'type_compte': 'AV',
                'total_retrait': self.montant_prestation
            })

        # return cotisation


    # Fonction workflow - Rejeter
    def compute_prestationssociale_rejet(self):
        self.statut_prestation = 'rejeter'

    # Fonction workflow - Annuler(Ramener à l'étape initial ou brouillon)
    def compute_prestationssocial_annul(self):
        self.statut_prestation = 'annuler'


    # La classe des intervenants du mutualiste
class DpsIntervenantMutualiste(models.Model):
    _name = 'dps.intervenant.mutualiste'
    _order = "id desc"
    _description = 'Les intervenants du mutualiste'

    # Champs sous onglets - Intervenant(s)
    intervenant = fields.Char(string='Personne Physique / Morale')
    typ_intervenant = fields.Selection([("adherent", "ADHERENT"),
                                        ("beneficiaire", "BENEFICIAIRE"),
                                        ("demandeur", "DEMANDEUR"),
                                        ("epoux_se", "EPOUX(SE)")])
    mont_intervenant = fields.Float(string="Montant")
    intervants_dps = fields.Many2one('dps_prestation_mutualiste', string='Prestations Sociales')


class DPSDocsPrestations(models.Model):
    _name = 'dps.documents.prestations'
    _order = "id desc"
    _description = 'Documents Des Prestations'

    typ_docs_prest = fields.Selection([("CNI_PREST","Carte National Identité (CNI)"),
                                 ("CM_PREST","Carte MUDCI"),
                                 ("CMU_PREST","Carte CMU"),
                                 ("PVCA_PREST","PV constat accident"),
                                 ("CGM_PREST","Certificat de genre de mort"),
                                 ("EAD_PREST","Extrait d'acte de décès"),
                                 ("CD_PREST","Certificat de décès"),
                                 ("ADN_PREST","Acte de notoriété")], string="Type De Document")
    ref_docs_prest = fields.Char("Référence Du Document") # Ref champs du fichier joint
    dat_valid_docs_prest = fields.Date("Date De Validité")
    dat_etablir_prest = fields.Datetime("Date établissement")
    dat_recept_prest = fields.Date("Date De Réception")
    attachment_docs_prest = fields.Binary("Document joint")  # Champ du fichier joint
    documents_mut_prest = fields.Many2one('dps_prestation_mutualiste', string="Document Des Prestations Du Mutualiste") # Many2One Documents Prestations