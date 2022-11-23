# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Solvera Branch Domain',
    'category': 'Stock',
    'author': 'Michael',
    'version': '1.0',
    'website': 'http://www.solvera.id/',
    'description': """
       Virtus Custom stock
    """,
    'data': [
        # 'security/branch_security.xml',
        # 'security/ir.model.access.csv',
        'views/res_partner_view.xml',

    ],
    "depends": [
        "stock","sale","contacts","multi_branch_base"
    ],
    'installable': True,
    "images":['static/logo.png'],
}
