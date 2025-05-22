from odoo import models, fields, api


class DpsCaissePrestation(models.Model):
    _name = 'dps.caisse.prestation'
    _order = "id desc"
    _description = 'Caisse Pestation'

    prest_auto_increment_caisse = fields.Char(string='Ref Prestation', readonly=True, store=True)
    mtt_enreg = fields.Float(string='Montant Payer', readonly=True)
    nom_mut_d = fields.Char(string='Nom', readonly=True)
    prenom_mut_d = fields.Char(string='Prenoms', readonly=True)
    cde_adh_mat_caisse = fields.Char(string='Matricule', readonly=True)
    statut_prestation_caisse = fields.Selection([("encreation", "En création"),
                                          ("enregistrer", "Enregistrer"),
                                          ("rejeter", "Suspendue"),
                                          ("appro_cs", "Approbation CS"),
                                          ("appro_cd", "Approbation CD"),
                                          ("appro_de", "Approbation DE"),
                                          ("valider", "Valider"),
                                          ("payer", "Payer")], readonly=True, string="Statut Prestation")
    dat_flux = fields.Datetime(string='Date de paiement', readonly=True, default=fields.Datetime.now)
    type_prestation_caisse = fields.Char(string='Type de Prestation', readonly=True)
