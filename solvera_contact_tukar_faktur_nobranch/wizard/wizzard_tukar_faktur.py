from odoo import fields,models,api
from datetime import datetime,date,timedelta
from odoo.exceptions import UserError
from num2words import num2words


class WizardTukarFaktur(models.TransientModel):
    _name = 'faktur.wizard'

    partner_id = fields.Many2one('res.partner',string='Customer',domain="[('parent_id', '=', False)]")
    partner_ids = fields.Many2many('account.move')
    name_sec = fields.Char("Name")

    

    @api.onchange('partner_id')
    def get_all_invoice(self):
        print('perint')
        if self.partner_id:
            print('perint',self.partner_id.name)
            temp=[]
            partner_obj = self.env['account.move'].search([('partner_id.parent_id','=',self.partner_id.id)
            ,('move_type','=','out_invoice')])
            for this in partner_obj:
                if this.move_type == "out_invoice":
                    temp.append(this.id)              
            self.partner_ids = [(6,0,temp)]
                
    
    def create_kwitansi(self):
        # print(data,'printtestdata')
             
        data = {
                    'model': 'faktur.wizard',
                    'form': self.read()[0]
                }
        
        invoice = self.partner_ids
        invoice_list = []
        today = date.today()
        for app in invoice:
            temp= + app.amount_total_signed
            terbilang = num2words(temp, lang='id')+" rupiah"
            vals = {
                'name': app.name,
                'due_date': app.invoice_date_due,
                'total': app.amount_total_signed,
                'terbilang': terbilang,
                'grand_total':temp,
                'partner':app.partner_id,
                'inv_name':self.name_sec,
                'now': today,

            }
            invoice_list.append(vals)
        # print("appointments", appointments)
        data['invoice'] = invoice_list
        return self.env.ref('solvera_contact_tukar_faktur_nobranch.report_kwitansi').report_action(self, data=data)