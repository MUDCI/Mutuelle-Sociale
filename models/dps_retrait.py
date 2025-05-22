from odoo import models, fields, api

class Retrait(models.Model):
    _name = 'dps.retrait'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Retrait'

    montant = fields.Float(string="Montant", required=True)
    type_compte = fields.Selection([
        ('mudci', 'Contribution au budget de la mudci'),
        ('AV', 'Assurance Vie'),
        ('AS', 'Assurance Santé'),
        ('FDS', 'Fonds De Solidarité'),
        ('SFE', 'SFE'),
        ('RETRAITE', 'Cotisation Mudci Rétraite'),
    ], string="Type de Compte", required=True)

    @api.model
    def create(self, vals):
        retrait = super(Retrait, self).create(vals)

        # Vérifier si une entrée pour ce type de retrait existe déjà du depot
        entree = self.env['dps_comptes'].search([
            ('type_compte', '=', retrait.type_compte)
        ], limit=1)

        if entree:
            # Mise à jour du montant existant (ajout du nouveau montant)
            entree.write({
                'total_retrait': entree.total_retrait + retrait.montant
            })
        else:
            # Création d'une nouvelle entrée
            self.env['dps_comptes'].create({
                'type_compte': retrait.type_compte,
                'total_retrait': retrait.montant
            })

        return retrait


    def unlink(self):
        for retrait in self:

            # MISE À JOUR DU MODÈLE `AutreModele`entreecompte
            entreecompte = self.env['dps_comptes'].search([
                ('type_compte', '=', retrait.type_compte)
            ], limit=1)

            if entreecompte:
                nouveau_total = entreecompte.total_retrait - retrait.montant
                if nouveau_total > 0:
                    entreecompte.write({'total_retrait': nouveau_total})
                else:
                    entreecompte.unlink()

        return super(Retrait, self).unlink()