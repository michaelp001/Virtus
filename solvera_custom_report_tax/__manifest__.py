# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Solvera_custom_report_tax',
    'category': 'report',
    'author': 'Michael',
    'version': '1.0',
    'website': 'http://www.solvera.id/',
    'description': """
       solvera custom report for Odoo14
    """,
    'data': [
        'security/ir.model.access.csv',
        'wizard/journal_excel.xml',
        'wizard/sale_wizard.xml',
        'wizard/excel_wizard.xml',



        
        
        

    ],
    'depends': [
                'account',
                

                ],
    'installable': True,
    "images":['static/logo.png'],
}
