# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Stock Picking UOM',
    'category': 'stock',
    'author': 'Michael',
    'version': '1.0',
    'website': 'http://www.solvera.id/',
    'description': """
      Partner Account Move
    """,
    'data': [
        # 'security/ir.model.access.csv',
        'views/stock_picking.xml',
        'views/stock_picking_wizard.xml',

    ],
    "depends": ["stock"],
    'installable': True,
    "images":['static/logo.png'],
}
