# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Replace_std_price',
    'category': 'purchase',
    'author': 'Michael',
    'version': '1.0',
    'website': 'http://www.solvera.id/',
    'description': """
       3 Difference Cost
    """,
    'data': [
        # 'security/ir.model.access.csv',
        'views/stock_quant_view.xml',
        'views/prodcut_template.xml',

    ],
    "depends": [
        "purchase","multi_branch_base","stock","stock_account",
    ],
    'installable': True,
    "images":['static/logo.png'],
}
