# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Solvera Fixing iNOVICE',
    'category': 'Asset',
    'author': 'Michael',
    'version': '1.0',
    'website': 'http://www.solvera.id/',
    'description': """
      Partner Account Move
    """,
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/asset_views.xml',

    ],
    "depends": [
        "stock","base_accounting_kit"
    ],
    'installable': True,
    "images":['static/logo.png'],
}
