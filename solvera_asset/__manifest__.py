# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Solvera Asset Date Collector',
    'category': 'Asset',
    'author': 'Michael',
    'version': '1.0',
    'website': 'http://www.solvera.id/',
    'description': """
      add on asset date collector
    """,
    'data': [
        # 'security/ir.model.access.csv',
        'views/asset_views.xml',

    ],
    "depends": [
        "purchase","base_accounting_kit","multi_branch_base"
    ],
    'installable': True,
    "images":['static/logo.png'],
}
