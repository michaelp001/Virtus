# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Solvera Branch Domain',
    'category': 'Stock',
    'author': 'Michael',
    'version': '1.0',
    'website': 'http://www.solvera.id/',
    'description': """
       User limitation (only can see his branch on contact)
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
