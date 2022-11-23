# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Solvera Module Anggaran',
    'category': 'NGO',
    'author': 'Michael',
    'version': '1.0',
    'website': 'http://www.solvera.id/',
    'description': """
       Solvera N G O
    """,
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/res_partner_view.xml',

    ],
    "depends": [
        "account","project"
    ],
    'installable': True,
    "images":['static/logo.png'],
}
