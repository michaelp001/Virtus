# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Solvera Manufacture Journal',
    'category': 'stock',
    'author': 'Michael',
    'version': '1.0',
    'website': 'http://www.solvera.id/',
    'description': """
      add manufacture journal (ALBA,AOP)
    """,
    'data': [
        # 'security/ir.model.access.csv',
        'views/product_views.xml',

    ],
    "depends": [
        "stock","base_accounting_kit"
    ],
    'installable': True,
    "images":['static/logo.png'],
}
