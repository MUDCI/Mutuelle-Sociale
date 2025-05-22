# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
import os
import base64

from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class Mutualiste(models.Model):
    _name = 'dps_mutualiste'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "id desc"
    _description = 'Mutualiste'
    _rec_name = "nom_prenoms"
    _rec_names_search = ['Cde_ID', 'Cde_Mat', 'surname_mut', 'nom_prenoms']

    Cde_Mat = fields.Char("Matricule")
    Cde_ID = fields.Char("Code Identifiant")
    surname_mut = fields.Char("Nom")
    lastname_mut = fields.Char("Prénoms")
    nom_prenoms = fields.Char(string="Nom et Prénoms", compute="_compute_name_lastname", store=True)
    datnaiss_mut = fields.Date("Date De Naissance")
    genr_mut = fields.Selection([("femme", "Femme"), ("homme", "Homme")], string="Genre")
    mail_mut = fields.Char("Email")
    adress_mut = fields.Char("Adresse")
    tel_mut = fields.Char("Telephone")
    mob_mut = fields.Char("Mobile")
    local_mut = fields.Char("Localité")
    etat_mut = fields.Boolean("Etat")
    statut_mut = fields.Char("Statut Mutualiste", default="Adherent")
    # photomutualiste = fields.Image("Photo")
    image = fields.Binary(string="Image", attachment=True)
    dps_revenu_mut = fields.One2many('dps_revenu', 'revenu_mut', string="Revenue Mutualiste", invisible=True)
    dps_docs_mut = fields.One2many('dps.docs.mutualiste', 'documents_mut', string="Documents Du Mutualiste")
    dps_engagement_mut = fields.One2many('dps.engagements.mutualiste', 'engagement_mut', string="Engagement Mutualiste")
    ayantdroits_ids = fields.One2many('dps.beneficiaire', 'code_mutualiste', string='ID AYANTS DROIT')
    pret_ids = fields.One2many('dps.prets', 'adherent_id', string='Prêts du Mutualiste')


    _sql_constraints = [
        ('code_unique_uniq', 'unique(Cde_ID)', 'Ce code doit être unique !')
    ]

    @api.constrains('Cde_ID')
    def _check_unique_code(self):
        for record in self:
            if self.search_count([('Cde_ID', '=', record.Cde_ID)]) > 1:
                raise ValidationError("Ce code doit être unique !")



    def action_import_image(self):
        repertoire_images = "C:/workspace/photos"

        if os.path.exists(repertoire_images) and os.path.isdir(repertoire_images):
            for nom_fichier in os.listdir(repertoire_images):
                chemin_fichier = os.path.join(repertoire_images, nom_fichier)

                if os.path.isfile(chemin_fichier):
                    # Extraire le nom sans l'extension (ex: "john_doe.jpg" -> "john_doe")
                    nom_sans_extension = os.path.splitext(nom_fichier)[0]

                    # Trouver l'enregistrement correspondant
                    mutualiste = self.search([('Cde_ID', '=', nom_sans_extension)], limit=1)

                    if mutualiste:
                        with open(chemin_fichier, "rb") as f:
                            image_data = base64.b64encode(f.read())

                        # Mettre à jour l'image de l'enregistrement existant
                        mutualiste.write({'image': image_data})

                    # with open(chemin_fichier, "rb") as f:
                    #     image_data = base64.b64encode(f.read())
                    #
                    # # Créer un enregistrement avec l'image
                    # self.create({
                    #     'Cde_ID': nom_fichier,
                    #     'image': image_data
                    # })
        else:
            raise FileNotFoundError(f"Le dossier '{repertoire_images}' est introuvable.")

    # Concatenation de nom et prénoms
    @api.depends('surname_mut', 'lastname_mut')
    def _compute_name_lastname(self):
        for record in self:
            record.nom_prenoms = f"{record.surname_mut or ''} {record.lastname_mut or ''}".strip()


# La classe des revenu du mutualiste
class DpsRevenu(models.Model):
    _name = 'dps_revenu'
    _description = 'Les revenus du mutualiste'

    name = fields.Selection([("TS","Le TS"),
                                    ("PT","Prime Trimestrielle"),
                                    ("SLR","Salaire")], string="Source de Revenu")
    montantrevenu = fields.Float("Montant")
    revenu_mut = fields.Many2one('dps_mutualiste', string='Mutualiste')
    revenu_pret = fields.Many2one('dps.prets', string='Revenu')

    # La classe des revenues du mutualiste
# class DpsRevenuMutualiste(models.Model):
#     _name = 'dps.revenu.mutualiste'
#     _order = "id desc"
#     _description = 'Les revenus du mutualiste'
#     # _inherit = 'mudci.adherent'
#
#     scr_revenue = fields.Selection([("IDR","Indemnité de départ à la retraite"),
#                                     ("PDR","Prime de responsabilité"),
#                                     ("PL","Prime de logement"),
#                                     ("TS","Le TS"),
#                                     ("PT","Prime Trimestrielle"),
#                                     ("SLR","Salaire")], string="Source de Revenu")
#     montantrevenu = fields.Float("Montant")
#     revenu_mut = fields.Many2one('mudci.adherent', string='Mutualiste', invisible="1")


# La classe des documents du mutualiste
class DpsDocs(models.Model):
    _name = 'dps.docs.mutualiste'
    _order = "id desc"
    _description = 'Documents mutualiste'

    dat_recept = fields.Date("Date De Réception")
    ref_docs = fields.Char("Référence Du Document")
    typ_docs = fields.Selection([("CNI","Carte National Identité (CNI)"),
                                 ("AN","Acte / Extrait de naissance"),
                                 ("PJC","Pièces justificatives du crédit"),
                                 ("BP","Bulletin de prime"),
                                 ("CM","Carte MUDCI"),
                                 ("CMU","Carte CMU"),
                                 ("DP","Demande de prêt"),
                                 ("BS","Bulletin de salaire"),
                                 ("PVCA","PV constat accident"),
                                 ("CGM","Certificat de genre de mort"),
                                 ("EAD","Extrait d'acte de décès"),
                                 ("CD","Certificat de décès"),
                                 ("ADN","Acte de notoriété")], string="Type De Document")
    dat_etablir = fields.Datetime("Date établissement")
    dat_valid_docs = fields.Date("Date De Validité")
    active_docs = fields.Char("Activation", default="Oui")
    documents_mut = fields.Many2one('dps_mutualiste', string="Documents Mutualiste")


    # La classe des engagements antérieur du mutualiste
class DpsEngagementAnterieur(models.Model):
    _name = 'dps.engagements.mutualiste'
    _order = "id desc"
    _description = 'Engamenents Anterieur du mutualiste'

    creancier_partner = fields.Char("Créancier")
    tel_creancier = fields.Char("Téléphone")
    mail_creancier = fields.Char("Email")
    montant_engager = fields.Float("Montant Engager")
    engagement_mut = fields.Many2one('dps_mutualiste', string="Mutualiste", invisible="1")

