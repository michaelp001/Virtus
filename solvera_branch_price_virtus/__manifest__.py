# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Branch Price',
    'category': 'Stock',
    'author': 'Michael',
    'version': '1.0',
    'website': 'http://www.solvera.id/',
    'description': """
       TO Hide branch price for another branch, and UOM descriction
    """,
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/product_template_custom_view.xml',
        'views/sale_order_views.xml',
        'views/purchase_order_views.xml',

    ],
    "depends": [
        "stock","sale","solvera_contact_tukar_faktur",'purchase'
    ],
    'installable': True,
    "images":['static/logo.png'],
}
