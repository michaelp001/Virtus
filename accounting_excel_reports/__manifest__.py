# -*- coding: utf-8 -*-
# License: Odoo Proprietary License v1.0

{
    'name': 'Odoo 14 Accounting Excel Reports',
    'version': '14.0.3.0.0',
    'category': 'Invoicing Management',
    'summary': 'Accounting Excel Reports, Odoo Excel Reports, Odoo Accounting Excel Reports, Odoo Financial Reports, '
               'Accounting Reports In Excel For Odoo 14, Financial Reports in Excel, Odoo Account Reports',
    'description': 'Accounting Excel Reports, Odoo Excel Reports, Odoo Accounting Excel Reports, Odoo Financial Reports, '
               'Accounting Reports In Excel For Odoo 14, Financial Reports in Excel, Odoo Account Reports',
    'sequence': '5',
    'live_test_url': 'https://www.youtube.com/watch?v=pz83Q9dobOM',
    'author': 'Odoo Mates',
    'company': 'Odoo Mates',
    'maintainer': 'Odoo Mates',
    'support': 'odoomates@gmail.com',
    'license': "OPL-1",
    'price': 30.00,
    'currency': 'USD',
    'website': '',
    'depends': ['accounting_pdf_reports'],
    'images': ['static/description/banner.gif'],
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'report/report.xml',
        'wizard/account_excel_reports.xml',
        'views/settings.xml',
        'views/templates.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}
