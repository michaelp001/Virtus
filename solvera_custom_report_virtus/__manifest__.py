# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Custom Report Virtus',
    'category': 'Reports',
    'author': 'Michael',
    'version': '1.0',
    'website': 'http://www.solvera.id/',
    'description': """
       Virtus Custom Contact
    """,
    'data': [
        # 'security/ir.model.access.csv',
        'reports/reports.xml',
        'reports/virtus_delivery_slip.xml',
        'reports/virtus_invoice.xml',
        'reports/custom_purchase_order.xml',
        'reports/virtus_proforma_invoice.xml',
        'reports/custom_sales_order.xml',
        'reports/virtus_internal_transfer.xml',
        'views/invoice_view.xml',

    ],
    "depends": [
        "sale","stock","solvera_delivery_time_stamp"
    ],
    'installable': True,
    "images":['static/logo.png'],
}
