# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Solvera Stamp Deliveru',
    'category': 'Contact',
    'author': 'Michael',
    'version': '1.0',
    'website': 'http://www.solvera.id/',
    'description': """
       Virtus Custom Contact
    """,
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/res_partner_view.xml',
        # 'views/purchase_order_views.xml',
        # 'views/sale_order_views.xml',
        'views/stock_picking_views.xml',

    ],
    "depends": [
        "sale",'solvera_contact_tukar_faktur'
    ],
    'installable': True,
    "images":['static/logo.png'],
}
