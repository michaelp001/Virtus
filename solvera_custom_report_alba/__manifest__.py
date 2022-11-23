# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Custom Report alba',
    'category': 'Reports',
    'author': 'Michael',
    'version': '1.0',
    'website': 'http://www.solvera.id/',
    'description': """
       alba Custom Report
    """,
    'data': [
        # 'security/ir.model.access.csv',
        'reports/reports.xml',
        'reports/alba_delivery_slip.xml',
        'reports/alba_invoice.xml',
        'reports/custom_purchase_order.xml',
        'reports/alba_proforma_invoice.xml',
        'reports/custom_sales_order.xml',
        'reports/alba_internal_transfer.xml',
        'views/invoice_view.xml',

    ],
    "depends": [
        "sale","stock","solvera_delivery_time_stamp_nobranch"
    ],
    'installable': True,
    "images":['static/logo.png'],
}
