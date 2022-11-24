# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'solvera product available',
    'category': 'Contact',
    'author': 'Michael',
    'version': '1.0',
    'website': 'http://www.solvera.id/',
    'description': """
      information for how much product available
    """,
    'data': [
        # 'security/ir.model.access.csv',
        'views/stock_picking.xml',

    ],
    "depends": [
        "purchase",
    ],
    'installable': True,
    "images":['static/logo.png'],
}
