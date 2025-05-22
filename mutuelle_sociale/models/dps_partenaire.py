# -*- coding: utf-8 -*-

from odoo import models, fields, api
# from odoo.exceptions import ValidationError

class Partenaire(models.Model):
    _name = 'dps.partenaire'
    _order = "id desc"
    _description = 'Partenaire'

    denomination = fields.Char("Denomination")
    cod_partenaire = fields.Char("Code")
    email_partenaire = fields.Char("email")
    contacts_partenaire = fields.Char("contacts")
    type_partenaire = fields.Selection([('Fournisseur', 'Fournisseur'),
                                        ('Mutuelle', 'Mutuelle'),
                                        ('Magasin', 'Magasin'),
                                        ('Banque', 'Banque'),
                                        ('Autre', 'Autre')], string='Type Partenaire')
