# -*- coding: utf-8 -*-
{
    'name': "mutuelle_sociale",

    'summary': "Gestion de prestations sociales",

    'description': """
Gestion de prestations sociales MUDCI
    """,

    'author': "My Company",
    'website': "https://www.mudci.ci",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'website'],

    # always loaded
    'data': [
        'security/dps_security.xml',
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/dps_typeprestations_view.xml',
        'views/dps_typeprets_view.xml',
        'views/dps_typecotisation_view.xml',
        'views/dps_cotisation_normale_view.xml',
        'views/dps_typeutilisateur_view.xml',
        'views/dps_mutualiste_view.xml',
        'views/dps_beneficiaire_view.xml',
        'views/dps_comptes_view.xml',
        'views/dps_depot_view.xml',
        'views/dps_retrait_view.xml',
        'views/dps_prets_view.xml',
        'views/dps_partenaire_view.xml',
        'views/dps_prestations_view.xml',
        'views/dps_caisse_view.xml',
        'views/dps_caisse_prestation_view.xml',
        'views/menu.xml',
        # 'data/data_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            # 'acs_hms/static/src/js/hms_graph_field.js',
            # 'acs_hms/static/src/js/hms_graph_field.xml',
            # 'acs_hms/static/src/js/hms_graph_field.scss',
            'mutuelle_sociale/static/src/css/custom_kanban.css',
            # 'mutuelle_sociale/static/src/js/custom_kanban.js',
            # 'https://cdn.jsdelivr.net/npm/chart.js',
        ]
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
