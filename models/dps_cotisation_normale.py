# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CotisationNormale(models.Model):
    _name = 'dps_cotisation_normale'
    _inherit = ['mail.thread', 'mail.activity.mixin']
     # _order = "id desc"
    _description = 'Cotisation'

    name = fields.Char("Cotisation", default="Normal")
    mutualiste = fields.Selection([("fonctionaire", "Fonctionaire"), ("journalier", "Journalier"), ("agentmudci", "Agent Mudci")], default="fonctionaire", string="Mutualiste")
    source = fields.Selection([("primes", "Prime trimestrielle"), ("salaire", "Salaire"), ("ts", "TS")], default="primes", string="Source prélèvement")
    periode = fields.Selection([("janvier", "Janvier"), ("fevrier", "Fevrier"), ("mars", "Mars"), ("avril", "Avril"), ("mai", "Mai"), ("juin", "Juin"), ("juillet", "Juillet"), ("aout", "Aout"), ("septembre", "Septembre"), ("octobre", "Octobre"), ("novembre", "Novembre"), ("decembre", "Decembre")], default="janvier", string="Période")
    anneecotisation = fields.Char("Année de cotisation")
    effectif_cotisation = fields.Char("Effectif Aegnt")
    montantpreleve = fields.Char("Montant Prélévé")
    montantcotisation = fields.Float("Montant")
    date_cotisation = fields.Date("Date")
    type_cotisation = fields.Selection([
        ('mudci', 'Contribution au budget de la mudci'),
        ('AV', 'Assurance Vie'),
        ('AS', 'Assurance Santé'),
        ('FDS', 'Fonds De Solidarité'),
        ('SFE', 'SFE'),
        ('RETRAITE', 'Cotisation Mudci Rétraite'),
    ], string="Type de Cotisation")


    @api.model
    def create(self, vals):
        cotisation = super(CotisationNormale, self).create(vals)

        # Vérifier si une entrée pour ce type de cotisation existe déjà du depot
        entree = self.env['dps.depot'].search([
            ('type_compte', '=', cotisation.type_cotisation)
        ], limit=1)


        if entree:
            # Mise à jour du montant existant (ajout du nouveau montant)
            entree.write({
                'montant': entree.montant + cotisation.montantcotisation
            })
        else:
            # Création d'une nouvelle entrée
            self.env['dps.depot'].create({
                'type_compte': cotisation.type_cotisation,
                'montant': cotisation.montantcotisation
            })

        # Vérifier si une entrée pour ce type de cotisation existe déjà au niveau du compte
        entreecompte = self.env['dps_comptes'].search([
            ('type_compte', '=', cotisation.type_cotisation)
        ], limit=1)


        if entreecompte:
            # Mise à jour du montant existant (ajout du nouveau montant)
            entreecompte.write({
                'total_depot': entreecompte.total_depot + cotisation.montantcotisation
            })
        else:
            # Création d'une nouvelle entrée
            self.env['dps_comptes'].create({
                'type_compte': cotisation.type_cotisation,
                'total_depot': cotisation.montantcotisation
            })

        return cotisation

    def unlink(self):
        for cotisation in self:
            # MISE À JOUR DU MODÈLE `Entree`
            entree = self.env['dps.depot'].search([
                ('type_compte', '=', cotisation.type_cotisation)
            ], limit=1)

            if entree:
                nouveau_montant = entree.montant - cotisation.montantcotisation
                if nouveau_montant > 0:
                    entree.write({'montant': nouveau_montant})
                else:
                    entree.unlink()

            # MISE À JOUR DU MODÈLE `AutreModele`entreecompte
            entreecompte = self.env['dps_comptes'].search([
                ('type_compte', '=', cotisation.type_cotisation)
            ], limit=1)

            if entreecompte:
                nouveau_total = entreecompte.total_depot - cotisation.montantcotisation
                if nouveau_total > 0:
                    entreecompte.write({'total_depot': nouveau_total})
                else:
                    entreecompte.unlink()

        return super(CotisationNormale, self).unlink()




    def write(self, vals):
        res = super(CotisationNormale, self).write(vals)

        # Récupérer l'entrée liée
        entree = self.env['dps.depot'].search([('type_compte', '=', self.type_cotisation)], limit=1)

        if entree:
            entree.write({
                'montant': entree.montant + self.montantcotisation
            })

            # Récupérer l'entrée liée
        entreecompte = self.env['dps_comptes'].search([('type_compte', '=', self.type_cotisation)], limit=1)

        if entreecompte:
            entreecompte.write({
                'total_depot': entreecompte.total_depot + self.montantcotisation
            })

        return res