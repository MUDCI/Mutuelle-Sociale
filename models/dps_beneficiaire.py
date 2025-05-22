# -*- coding: utf-8 -*-
from email.policy import default
from symtable import Class

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging
import os
import base64

_logger = logging.getLogger(__name__)


# from odoo.exceptions import ValidationError

class DpsBeneficiaire(models.Model):
    _name = 'dps.beneficiaire'
    _description = 'Ligne des ayants droits du mutualiste'
    _inherit = 'dps_mutualiste'
    _rec_name = 'cde_benef'

    cde_benef = fields.Char("Code ID")
    # cde_mut_benef = fields.Char("Code ID Adhérent") # Le Code ID Adhérent à comparer
    nom_benef = fields.Char("Nom")
    prenoms_benef = fields.Char("Prénoms")
    datnaiss_benef = fields.Date("Date De Naissance")
    genr_benef = fields.Selection([("femme","Femme"),("homme","Homme")], string="Genre")
    statut_benef = fields.Selection([("conjoint","Conjoint"),("enfants","Enfant")], string="Statut Beneficiaire")
    local_benef = fields.Char("Localite")
    tel_benef = fields.Char("Telephone")
    etat_benef = fields.Boolean("Etat")
    activate_benef = fields.Char("Statut Mutualiste", default="Oui")
    code_mutualiste = fields.Many2one('dps_mutualiste', string="Adherent")
    # code_ = fields.Char("CODE MUTUALISTE", readonly=True, store=True, related="dps_mutualiste.Cde_ID")
    image_benef = fields.Binary(string="Image", attachment=True)

    _sql_constraints = [
        ('code_unique_uniq', 'unique(cde_benef)', 'Ce code doit être unique !')
    ]

    @api.constrains('cde_benef')
    def _check_unique_code(self):
        for record in self:
            if self.search_count([('cde_benef', '=', record.cde_benef)]) > 1:
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
                    beneficiaire = self.search([('cde_benef', '=', nom_sans_extension)], limit=1)

                    if beneficiaire:
                        with open(chemin_fichier, "rb") as f:
                            image_data = base64.b64encode(f.read())

                        # Mettre à jour l'image de l'enregistrement existant
                        beneficiaire.write({'image_benef': image_data})
        else:
            raise FileNotFoundError(f"Le dossier '{repertoire_images}' est introuvable.")