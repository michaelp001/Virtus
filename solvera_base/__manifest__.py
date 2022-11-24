# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Custom Contact',
    'category': 'Contact',
    'author': 'Michael',
    'version': '1.0',
    'website': 'http://www.solvera.id/',
    'description': """
       Base For Any Project SOlvera
    """,
    'data': [
        # 'security/ir.model.access.csv',
        'views/res_partner_view.xml',
        'views/purchase_order_views.xml',
        'views/sale_order_views.xml',
        'views/stock_picking_views.xml',

    ],
    "depends": [
        "sale",
    ],
    'installable': True,
    "images":['static/logo.png'],
}
