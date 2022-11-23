from odoo import fields,models,api
from datetime import datetime,date,timedelta
from odoo.exceptions import UserError
class SaleOrder(models.Model):
    _inherit = "sale.order"

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('approval', 'Need Approve'),
        ('approved', 'Approved'),
        ('cancel', 'Cancelled'),
        ('que', 'In Queue'),
        ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')

    partner_invoice_id = fields.Many2one(
        'res.partner', string='Invoice Address',
        readonly=True, required=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)], 'sale': [('readonly', False)]},
        domain="[('parent_id','=',partner_id)]")
    partner_shipping_id = fields.Many2one(
        'res.partner', string='Delivery Address', readonly=True, required=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)], 'sale': [('readonly', False)]},
        domain="[('parent_id','=',partner_id)]",)

    partner_id = fields.Many2one(
        'res.partner', string='Customer', readonly=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        required=True, change_default=True, index=True, tracking=1,
        domain="[('company_id', '=', company_id),('branch_id','=',branch_id)]")

    def approval_request(self):
        for i in self:
            template_id = self.env.ref('solvera_sale_approve.so_approval')
            template_id.send_mail(self.id,force_send=True)
            i.write({'state': 'approval'})

    def approved(self):
        for i in self:
            i.write({'state': 'approved'})
    def approved_cancel(self):
        for i in self:
            i.write({'state': 'draft'})

    
