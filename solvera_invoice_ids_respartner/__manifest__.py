# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Partner Account Move',
    'category': 'Contact',
    'author': 'Michael',
    'version': '1.0',
    'website': 'http://www.solvera.id/',
    'description': """
      Partner Account Move
    """,
    'data': [
        # 'security/ir.model.access.csv',
        'views/res_partner_views.xml',

    ],
    "depends": [
        "purchase",
    ],
    'installable': True,
    "images":['static/logo.png'],
}
