
import datetime
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime,timedelta

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ('approval', 'Need Approve'),
        ('approved', 'Approved'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)


            
    def approval_request(self):
        for i in self:
            i.write({'state': 'approval'})

    def approved(self):
        for i in self:
            i.write({'state': 'approved'})
    def approved_cancel(self):
        for i in self:
            i.write({'state': 'draft'})

    
   