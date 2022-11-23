# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Custom Report AOP',
    'category': 'Reports',
    'author': 'Michael',
    'version': '1.0',
    'website': 'http://www.solvera.id/',
    'description': """
       aop Custom Report
    """,
    'data': [
        # 'security/ir.model.access.csv',
        'reports/reports.xml',
        'reports/aop_delivery_slip.xml',
        'reports/aop_invoice.xml',
        'reports/custom_purchase_order.xml',
        'reports/aop_proforma_invoice.xml',
        'reports/custom_sales_order.xml',
        'reports/aop_internal_transfer.xml',
        'views/invoice_view.xml',

    ],
    "depends": [
        "sale","stock","solvera_delivery_time_stamp_nobranch"
    ],
    'installable': True,
    "images":['static/logo.png'],
}
