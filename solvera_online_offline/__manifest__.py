# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Solvera Sequence Branch',
    'category': 'Sales',
    'author': 'Michael',
    'version': '1.0',
    'website': 'http://www.solvera.id/',
    'description': """
       different between offline and online sales
    """,
    'data': [
        # 'security/ir.model.access.csv',
        # 'reports/email.xml',
        # 'views/sale_view.xml',
        'views/stock_location.xml',
        # 'data/ir_sequence.xml',
    ],
    "depends": [
        "sale",'multi_branch_base','contacts',"solvera_contact_information"
    ],
    'installable': True,
    "images":['static/logo.png'],
}
