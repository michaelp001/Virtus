# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle 
#
##############################################################################
{
    'name': 'Multiple Invoice Payment',
    'version': '14.0.1.0',
    'sequence':1,
    'description': """
        App will allow multiple invoice payment from payment and invoice screen.
        
       Multiple invoice payment, Invoice Multiple payment, Payment , Partial Invoice Payment, Full invoice Payment,Payment write off,   Payment Invoice, 
    Multiple invoice payment
    Credit notes payment
    How can create multiple invoice
Invoice Management 
Odoo Multiple Invoice Payment 
Odoo Invoice Management 
Multiple invoice payment
Credit notes payment
How can create multiple invoice
How can create multiple invoice odoo
Multiple invoice payment in single click
Make multiple invoice payment
Partial invoice payment
Credit note multiple payment
Pay multiple invoice
Paid multiple invoice
Invoice payment automatic
Invoice wise payment
Odoo invoice payment
Openerp invoice payment
Partial invoice
Partial payment
Pay partially invoice
Pay partially payment
Invoice generation
Invoice payment
Website payment receipt
Multiple bill payment
Multiple vendor bill payment
Vendor bill
Manage vendor bill 
Odoo manage vendor bill 
Vendor bill management 
Odoo Vendor bill management
Make Multiple Invoice Payment in single click
Odoo Make Multiple Invoice Payment in single click
Select Multiple invoice then after make payment
Odoo Select Multiple invoice then after make payment
From payment screen select customer and system will load all open invoice to make payment.
Odoo From payment screen select customer and system will load all open invoice to make payment.
Full and Partial Invoice Payment
Odoo Full and Partial Invoice Payment
More then amount payment will be balance into customer account for next invoice redeem
Odoo More then amount payment will be balance into customer account for next invoice redeem
Process Credit Note Multiple Payment
Odoo Process Credit Note Multiple Payment
Select Multiple Invoice 
Odoo select multiple Invoice 
Manage selection of Multiple Invoice 
Odoo Manage Selection of Multiple Invoice 
Payment process 
Odoo payment process 
Paid multiple Invoice
Odoo Paid Multiple Invoice 
Multiple Invoice Payment 
Odoo Multiple Invoice Payment 
Manage multiple Invoice 
Odoo Manage Multiple Invoice 
Invoice Payment Journal Entry 
Odoo Invoice Payment Journal Entry 
Manage Invoice Payment Journal Entry 
Odoo Manage Invoice Payment Journal Entry 
    """,
    "category": 'Accounting',
    'summary': 'These apps use to easy payment multi invoice payment | multi-vendor bill payment mass invoice payment | mass bill payment | multiple invoice payment | multiple bill payment, multiple partial payment | multi-payment vendor bill | multiple payment vendor bills, multi invoice payment',
    'author': 'DevIntelle Consulting Service Pvt.Ltd', 
    'website': 'http://www.devintellecs.com',
    'depends': ['sale_management','account'],
    'data': [
            'security/ir.model.access.csv',
            'views/account_payment.xml',
            'wizard/bulk_invoice_payment.xml',
            ],
    'demo': [],
    'test': [],
    'css': [],
    'qweb': [],
    'js': [],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'price':35.0,
    'currency':'EUR',
    #'live_test_url':'https://youtu.be/A5kEBboAh_k',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
