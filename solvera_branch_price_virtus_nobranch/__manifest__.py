# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Solvera custom Pricelist for virtus nobranch',
    'category': 'Stock',
    'author': 'Michael',
    'version': '1.0',
    'website': 'http://www.solvera.id/',
    'description': """
       Virtus Custom stock
    """,
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/product_template_custom_view.xml',
        'views/sale_order_views.xml',
        'views/purchase_order_views.xml',

    ],
    "depends": [
        "sale","stock","solvera_contact_tukar_faktur_nobranch"
    ],
    'installable': True,
    "images":['static/logo.png'],
}
