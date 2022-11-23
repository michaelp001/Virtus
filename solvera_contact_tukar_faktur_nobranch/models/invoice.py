from email.policy import default
from odoo import fields,models,api
from datetime import datetime,date,timedelta
from odoo.exceptions import UserError

class CustomInvoiceModule(models.Model):
    _inherit = "account.move"

    picking_ids = fields.Many2many("stock.picking","invoice_picking_rell","picking_id","alm_id",compute='_compute_picking_ids')
    po_customer = fields.Char(string='Notes Customer',related="invoice_line_ids.po_customer")
    date_deadline=fields.Date(string="Date End",compute="onchange_enddate",readonly=False)
    allow_tukar_fakur= fields.Boolean(string="Customer Tukar Faktur",related="partner_id.tukar_faktur_allow",readonly='1')
    tanggal_tukar_faktur = fields.Date(string="Tanggal Tukar Faktur")
    picking = fields.Char(string='Picking ID',related="invoice_line_ids.picking")
    picking_date = fields.Datetime(string="Delivery Date", related="invoice_line_ids.picking_date")
    date_validate = fields.Date(string="Tanggal Diterima", related="invoice_line_ids.date_validate")
    state_sale = fields.Selection([
    ('0', 'Offline'),
    ('1', 'Tokopedia'),
    ('2', 'Shopee'),
    ('3', 'Lazada'),
    ('4', 'Web'),
    ], string='Sumber Penjualan', readonly=False, copy=False, related="invoice_line_ids.state_sale")


    def write(self,vals):
        for i in self:
            term = i.invoice_payment_term_id.line_ids
            allow_tukar_fakur = vals.get('allow_tukar_fakur') or i.allow_tukar_fakur
            tanggal_tukar_faktur = vals.get('tanggal_tukar_faktur') 
        
            if allow_tukar_fakur == True and tanggal_tukar_faktur:
                tanggal_tukar_faktur = datetime.strptime(tanggal_tukar_faktur,'%Y-%m-%d')
                if tanggal_tukar_faktur:
                    tanggal_tukar_faktur = tanggal_tukar_faktur.date()
                    vals['invoice_date_due'] = tanggal_tukar_faktur + timedelta(term.days)
        res = super(CustomInvoiceModule, self).write(vals)
       
        return res


    def action_post(self):
 
        res = super(CustomInvoiceModule, self).action_post()
        for this in self:
            if this.move_type in ['out_invoice','entry'] and this.allow_tukar_fakur == False :
                term = self.invoice_payment_term_id.line_ids
                if this.date_validate:
                    if this.invoice_date == None:
                        this.invoice_date = this.date_validate
                        this.date = this.invoice_date if this.invoice_date else this.date
                        this.invoice_date_due = (this.invoice_date + timedelta(term.days)) if this.invoice_date else this.invoice_date
                    else:
                        this.invoice_date =this.date_validate
                        this.date = this.invoice_date if this.invoice_date else this.date
                        this.invoice_date_due = (this.invoice_date + timedelta(term.days)) if this.invoice_date else this.invoice_date

            elif this.move_type in ['out_invoice','entry'] and this.allow_tukar_fakur == True :
                term = self.invoice_payment_term_id.line_ids
                if this.date_validate:
                    if this.invoice_date == None:
                        this.invoice_date = this.date_validate
                        this.date = this.invoice_date if this.invoice_date else this.date
                        this.invoice_date_due = (this.invoice_date + timedelta(term.days)) if this.invoice_date else this.invoice_date
                    else:
                        this.invoice_date = this.date_validate
                        this.date = this.invoice_date if this.invoice_date else this.date
                        this.invoice_date_due = (this.invoice_date + timedelta(term.days)) if this.invoice_date else this.invoice_date

        for i in self:
            for inv in i.invoice_line_ids:
                for line in i.line_ids:
                    if i.state_sale == '1':
                        if inv.product_id.categ_id.property_account_expense_categ_id == line.account_id:
                            line.update({
                                                'account_id': line.product_id.categ_id.property_account_expense_toped_categ_id,
                                            })
                        if i.branch_id.id==1:
                            i.journal_id.id == 59
                        if i.branch_id.id==2:
                            i.journal_id.id == 63
                        if i.branch_id.id==3:
                            i.journal_id.id == 67


                    if i.state_sale == '2':
                        if inv.product_id.categ_id.property_account_expense_categ_id == line.account_id:
                            line.update({
                                                'account_id': line.product_id.categ_id.property_account_expense_shoppe_categ_id,
                                            })
                        if i.branch_id.id==1:
                            i.journal_id.id == 60
                        if i.branch_id.id==2:
                            i.journal_id.id == 64
                        if i.branch_id.id==3:
                            i.journal_id.id == 68
                    if i.state_sale == '3':
                        if inv.product_id.categ_id.property_account_expense_categ_id == line.account_id:
                            line.update({
                                                'account_id': line.product_id.categ_id.property_account_expense_lazada_categ_id,
                                            })
                        if i.branch_id.id==1:
                            i.journal_id.id == 61
                        if i.branch_id.id==2:
                            i.journal_id.id == 65
                        if i.branch_id.id==3:
                            i.journal_id.id == 69
                        
                    if i.state_sale == '4':
                        if inv.product_id.categ_id.property_account_expense_categ_id == line.account_id:
                            line.update({
                                                'account_id': line.product_id.categ_id.property_account_expense_web_categ_id,
                                            })
                        if i.branch_id.id==1:
                            i.journal_id.id == 62
                        if i.branch_id.id==2:
                            i.journal_id.id == 66
                        if i.branch_id.id==3:
                            i.journal_id.id == 70
                
        return res

    

    def update_invoice_date_to_date(self):
        for this in self.search([('move_type','=','entry')]):
            if this.invoice_date:
                this.date = this.invoice_date
                
    
    def onchange_enddate(self):
        term = self.invoice_payment_term_id.line_ids
        if self.invoice_date:
            self.date_deadline = self.invoice_date_due 
    
    @api.depends('invoice_line_ids')
    def _compute_picking_ids(self):
    	for this in self:
            picking_ids = this.invoice_line_ids.mapped('picking_ids')
            if picking_ids:
                picking_ids = picking_ids.ids
            else:
                picking_ids = []
            this.picking_ids = [(6,0,picking_ids)]

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    picking_ids = fields.Many2many('stock.picking')
    picking_line_ids = fields.Many2many('stock.move')
    picking = fields.Char()
    po_customer = fields.Char()
    picking_date = fields.Datetime()
    date_validate = fields.Date()
    fix_discount = fields.Float()
    is_fix_discount = fields.Boolean()
    state_sale = fields.Selection([
    ('0', 'Offline'),
    ('1', 'Tokopedia'),
    ('2', 'Shopee'),
    ('3', 'Lazada'),
    ('4', 'Web'),
    ], string='Sumber Penjualan', readonly=False, copy=False,default="0")

class StockMove(models.Model):
    _inherit = 'stock.move'

    invoice_id = fields.Many2one('account.move','No. Invoice')
    invoice_line_id = fields.Many2one('account.move.line')
    date_terima = fields.Date(related='picking_id.tanggal_diterima')

    def _create_account_move_line(self, credit_account_id, debit_account_id, journal_id, qty, description, svl_id, cost):
        self.ensure_one()
        AccountMove = self.env['account.move'].with_context(default_journal_id=journal_id)

        move_lines = self._prepare_account_move_line(qty, cost, credit_account_id, debit_account_id, description)
        if move_lines:
            if self.date_terima :
                new_account_move = AccountMove.sudo().create({
                    'journal_id': journal_id,
                    'line_ids': move_lines,
                    'date': self.date_terima,
                    'ref': description,
                    'stock_move_id': self.id,
                    'stock_valuation_layer_ids': [(6, None, [svl_id])],
                    'move_type': 'entry',
                })
                new_account_move._post()
            else:
                date = self._context.get('force_period_date', fields.Date.context_today(self))
                new_account_move = AccountMove.sudo().create({
                    'journal_id': journal_id,
                    'line_ids': move_lines,
                    'date': date,
                    'ref': description,
                    'stock_move_id': self.id,
                    'stock_valuation_layer_ids': [(6, None, [svl_id])],
                    'move_type': 'entry',
                })
                new_account_move._post()
