# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Solvera Manual Faktur no branch',
    'category': 'Contact',
    'author': 'Michael',
    'version': '1.0',
    'website': 'http://www.solvera.id/',
    'description': """
       juset add manual facture without branch
    """,
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_move.xml',
        # 'views/purchase_order_views.xml',
        # 'views/sale_order_views.xml',


    ],
    "depends": [
        "sale"
    ],
    'installable': True,
    "images":['static/logo.png'],
}
