# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Hide Value ',
    'category': 'Contact',
    'author': 'Michael',
    'version': '1.0',
    'website': 'http://www.solvera.id/',
    'description': """
       hide value
    """,
    'data': [
        # 'security/ir.model.access.csv',
        'views/stock_quant.xml',

    ],
    "depends": [
        "sale",
    ],
    'installable': True,
    "images":['static/logo.png'],
}
