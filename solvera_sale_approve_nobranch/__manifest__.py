# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Solvera Sales Approval',
    'category': 'Sales',
    'author': 'Michael',
    'version': '1.0',
    'website': 'http://www.solvera.id/',
    'description': """
       Approval in sales no branch
    """,
    'data': [
        # 'security/ir.model.access.csv',
        'reports/email.xml',
        'views/sale_view.xml',
        'views/purchase_view.xml',

    ],
    "depends": [
        "sale","contacts","solvera_contact_tukar_faktur_nobranch"
    ],
    'installable': True,
    "images":['static/logo.png'],
}
