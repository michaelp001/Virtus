# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle 
#
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import itertools
from operator import itemgetter
import operator
from datetime import datetime

class bulk_invoice(models.TransientModel):
    _name = 'bulk.invoice'
    _description = 'Bulk Invoice'
    
    invoice_id = fields.Many2one('account.move',string='Invoice')
    partner_id = fields.Many2one('res.partner',string='Partner')
    amount = fields.Float('Amount')
    paid_amount = fields.Float('Pay Amount') 
    bulk_invoice_id = fields.Many2one('bulk.inv.payment')
    
class bulk_inv_payment(models.TransientModel):
    _name = 'bulk.inv.payment'
    _description = 'Bulk invoice payment'
    
    @api.model
    def default_get(self,fields):
        res={}
        inv_ids = self._context.get('active_ids')
        vals=[]
        invoice_ids = self.env['account.move'].browse(inv_ids)
        inv_type = ''
        for invo in invoice_ids:
            inv_type = invo.move_type
            break
        for inv in invoice_ids:
            if inv_type != inv.move_type:
                raise ValidationError('You must select only invoices or refunds.')
            if inv.state == 'draft' or inv.payment_state == 'paid':
                raise ValidationError('Please Select posted or unpaid invoice...')
            vals.append((0,0,{
                'invoice_id':inv and inv.id or False,
                'partner_id':inv and inv.partner_id.id or False,
                'amount':inv.amount_residual or 0.0,
                'paid_amount':inv.amount_residual or 0.0,
            }))
            if inv.move_type in ('out_invoice','out_refund'):
                res.update({
                    'partner_type':'customer',
                })
            else:
                res.update({
                    'partner_type':'supplier',
                })
        if inv_type in ('out_invoice','in_refund'):
            res.update({
                'payment_type':'inbound'
            })
        else:
            res.update({
                'payment_type':'outbound'
            })
        
        res.update({
        'invoice_ids':vals,
        })
        return res
    
    
    
    name = fields.Char('Name',default='hello')
    payment_type = fields.Selection([('outbound','Send Money'),('inbound','Receive Money'),('transfer','Transfer')],string="Payment Type", required="1")
    payment_date = fields.Date('Payment Date', required="1")
    communication = fields.Char('Memo')
    partner_type = fields.Selection([('customer','Customer'),('supplier','Supplier')],string='Partner Type')
    journal_id = fields.Many2one('account.journal', string='Payment Method', required=True, domain=[('type', 'in', ('bank', 'cash'))])
    invoice_ids = fields.One2many('bulk.invoice','bulk_invoice_id',string='Invoice')

    
    def process_payment(self):
        vals=[]
        for line in self.invoice_ids:
            if line.paid_amount > 0.0:
                vals.append({
                    'invoice_id':line.invoice_id or False,
                    'partner_id':line.partner_id and line.partner_id.id or False,
                    'amount':line.amount or 0.0,
                    'paid_amount':line.paid_amount or 0.0,
                    'currency_id':line.invoice_id.currency_id.id or False,
                })
        new_vals=sorted(vals,key=itemgetter('partner_id'))
        groups = itertools.groupby(new_vals, key=operator.itemgetter('partner_id'))
        result = [{'partner_id':k,'values':[x for x in v]} for k, v in groups]
        new_payment_ids=[]
        for res in result:
            payment_method_id= self.env['account.payment.method'].search([('name','=','Manual')],limit=1)
            if not payment_method_id:
                payment_method_id= self.env['account.payment.method'].search([],limit=1)
            payment_date = False
            if self.payment_date:
                payment_date = self.payment_date.strftime("%Y-%m-%d")
            pay_val={
                'payment_type':self.payment_type,
                'date':payment_date,
                'partner_type':self.partner_type,
                'payment_for':'multi_payment',
                'partner_id':res.get('partner_id'),
                'journal_id':self.journal_id and self.journal_id.id or False,
                'ref':self.communication,
                'payment_method_id':payment_method_id and payment_method_id.id or False,
                'state':'draft',
                'currency_id':res.get('values')[0].get('currency_id'),
                'amount':0.0,
            }
            payment_id = self.env['account.payment'].create(pay_val)
            line_list=[]
            paid_amt=0
            inv_ids = []
            for inv_line in res.get('values'):
                invoice  = inv_line.get('invoice_id')
                inv_ids.append(invoice.id)
                full_reco=False
                if invoice.amount_residual == inv_line.get('paid_amount'):
                    full_reco = True
                line_list.append((0,0,{
                    'invoice_id':invoice.id,
                    'date':invoice.invoice_date,
                    'due_date':invoice.invoice_date_due,
                    'original_amount':invoice.amount_total,
                    'balance_amount':invoice.amount_residual,
                    'allocation':inv_line.get('paid_amount'),
                    'full_reconclle':full_reco,
                    'account_payment_id':payment_id and payment_id.id or False
                }))
                paid_amt += inv_line.get('paid_amount')
            payment_id.write({
                'line_ids':line_list,
                'amount':paid_amt,
            })
            new_payment_ids.append(payment_id)
        for pay in new_payment_ids:
            pay.dev_generate_moves()
        return True
 
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
