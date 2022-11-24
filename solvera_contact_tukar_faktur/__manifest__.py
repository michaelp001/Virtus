# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Tukar Faktur',
    'category': 'Contact',
    'author': 'Michael',
    'version': '1.0',
    'website': 'http://www.solvera.id/',
    'description': """
       Sistem tukar faktur dimana due date akan diperpanjang sesuai dengan tukar faktur
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_view.xml',
        'views/sale_order_views.xml',
        'views/picking_view.xml',
        'views/invoice_view.xml',
        'views/product_categ.xml',
        'views/uom_views.xml',
        'wizard/tukar_faktur.xml',
        'reports/reports.xml',
        'reports/report_kwitansi_gabungan.xml',
    ],
    "depends": [
        "sale","solvera_sequence_branch","solvera_contact_information"
    ],
    'installable': True,
    "images":['static/logo.png'],
}
