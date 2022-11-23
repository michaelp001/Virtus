from odoo import fields,models,api,_
from datetime import datetime,date
from odoo.exceptions import ValidationError, UserError
from openerp.exceptions import UserError
import base64
import io
from datetime import datetime
import xlsxwriter
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class WizCommission(models.TransientModel):
    _name = 'sale.wizard'

    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date to')
    invoice_line_ids = fields.Many2many('account.move')
    filename = fields.Char(size=256, readonly=True)
    data_binary = fields.Binary('Content Data', readonly=True)
    # salesperson = fields.Many2one('res.users')


    def export_sale(self):

        query = """
            SELECT DISTINCT ON (aml.id) aml.id as line_id,	am.invoice_date as dates, am.name as invoice, rp.name as partner_id,
                ptemp.name as product_id, ptemp.default_code as product_code ,
                aml.price_unit, aml.discount, aml.quantity,am.state, am.payment_state,
                am.move_type, rp.kode, am.amount_total, am.amount_tax as ppn
                ,round(am.amount_total+am.amount_tax) as total, aml.price_subtotal as subtotal,
                round(aml.price_unit*aml.quantity-aml.price_subtotal,0) as diskon, am.amount_untaxed
                rp, aml.picking, am.invoice_origin, am.invoice_date ,am.payment_state
                ,ru.login, team.name ,ap.create_date AS date_create, aml.picking_date AS picking_date
                ,so.date_order AS order_date, uu.name as uu , am.payment_reference as refe, 
                TO_CHAR(am.invoice_date_due, 'DD-MM-YYYY') as dates_due,pc.name as categ,rpp.internal_name as parent ,rpp.state_sale as sale
        FROM account_move_line aml
            JOIN account_move am on aml.move_id =am.id
            LEFT JOIN res_partner rp on am.partner_id = rp.id
            LEFT JOIN res_partner rpp on rp.parent_id = rpp.id
            LEFT JOIN res_users ru on am.invoice_user_id = ru.id
            LEFT JOIN crm_team team on am.team_id = team.id
            LEFT JOIN product_product product on aml.product_id = product.id
            LEFT JOIN product_template ptemp on product.product_tmpl_id = ptemp.id
                LEFT JOIN product_category pc on ptemp.categ_id = pc.id
            LEFT JOIN uom_uom uu on ptemp.uom_id = uu.id
            LEFT JOIN account_move am2 ON am2.ref = am.name
            LEFT JOIN account_payment ap ON am2.id = ap.move_id
            LEFT JOIN sale_order so ON am.invoice_origin =so.name
        WHERE am.move_type in ('out_refund','out_invoice') and aml.partner_id is not null  AND am.state != 'cancel' and aml.product_id is not null and aml.price_unit > 0 and aml.is_anglo_saxon_line is null and am.invoice_date >= %s AND am.invoice_date <= %s 
            ORDER BY line_id
        """
        params = (self.date_from, self.date_to,)
        self.env.cr.execute(query,params)
        pick_ids = self.env.cr.dictfetchall()


        bz_data = io.BytesIO()
        workbook = xlsxwriter.Workbook(bz_data)
        filename = 'Activity.xls'
        
        sheet = workbook.add_worksheet('Journal')
        sheet.set_column('A:A', 10)
        sheet.set_column('B:B', 15)
        sheet.set_column('C:C', 15)
        sheet.set_column('D:D', 50)
        sheet.set_column('E:E', 35)
        sheet.set_column('F:F', 15)
        sheet.set_column('G:G', 17)
        sheet.set_column('H:H', 15)
        sheet.set_column('I:I', 20)
        sheet.set_column('J:J', 17)
        sheet.set_column('K:K', 17)
        sheet.set_column('L:L', 25)
        sheet.set_column('M:M', 30)
        sheet.set_column('N:N', 50)
        sheet.set_column('O:O', 10)
        sheet.set_column('P:P', 10)
        sheet.set_column('Q:Q', 10)
        sheet.set_column('R:R', 10)
        sheet.set_column('S:S', 10)
        sheet.set_column('T:T', 10)
        sheet.set_column('U:U', 15)
        sheet.set_column('V:V', 25)
        sheet.set_column('W:W', 20)
        sheet.set_column('X:X', 20)
        sheet.set_column('Y:Y', 20)
    
        ################## style ##################
        number_center = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
        number_center.set_font_name('Arial')
        number_center.set_font_size('11')
        number_center.set_border()
        number_center.set_text_wrap()
        ###########################################
        normal_center = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'bold': 1})
        normal_center.set_font_name('Arial')
        normal_center.set_font_size('11')
        normal_center.set_text_wrap()
        ###########################################
        normal_left = workbook.add_format({'align': 'left'})
        normal_left.set_font_name('Arial')
        normal_left.set_font_size('11')
        normal_left.set_border()
        normal_left.set_text_wrap()
        ###########################################
        normal_center_border = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'bold': 1})
        normal_center.set_font_name('Arial')
        normal_center_border.set_font_size('11')
        normal_center_border.set_border()
        normal_center_border.set_text_wrap()
        ###########################################
        normal_left_border = workbook.add_format({'align': 'left', 'valign': 'vleft', 'bold': 0})
        normal_left_border.set_font_name('Arial')
        normal_left_border.set_font_size('11')
        normal_left_border.set_border()
        normal_left_border.set_text_wrap()
        ###########################################
        date_format = workbook.add_format({'num_format': 'dd/mm/yy'})
        date_format.set_font_name('Arial')
        date_format.set_font_size('11')
        date_format.set_border()
        date_format.set_text_wrap()
        ###########################################
        s_date = datetime.strftime(self.date_from, "%d-%b-%y")
        e_date = datetime.strftime(self.date_to, "%d-%b-%y")
        format2 = workbook.add_format({'num_format': 'dd/mm/yy'})
        sheet.write('A1', 'No', normal_center_border)
        sheet.write('B1', 'Tanggal Invoice', normal_center_border)
        sheet.write('C1', 'NAMA CUSTOMER', normal_center_border)
        sheet.write('D1', 'INTERNAL NAME', normal_center_border)
        sheet.write('E1', 'SUMBER PENJUALAN', normal_center_border)
        sheet.write('F1', 'Nomor SO', normal_center_border)
        sheet.write('G1', 'Tanggal SO', normal_center_border)
        sheet.write('H1', 'Nomor DO', normal_center_border)
        sheet.write('I1', 'Tanggal DO', normal_center_border)
        sheet.write('J1', 'Nomor Invoice', normal_center_border)
        sheet.write('K1', 'Payment Reference', normal_center_border)
        sheet.write('L1', 'KODE BARANG', normal_center_border)
        sheet.write('M1', 'NAMA BARANG', normal_center_border)
        sheet.write('N1', 'UOM', normal_center_border)
        sheet.write('O1', 'QTY', normal_center_border)
        sheet.write('P1', 'HARGA', normal_center_border)
        sheet.write('Q1', 'DISC', normal_center_border)
        sheet.write('R1', 'TOTAL', normal_center_border)
        sheet.write('S1', 'Status AR', normal_center_border)
        sheet.write('T1', 'Tanggal Pelunasan', normal_center_border)
        sheet.write('U1', 'Salesperson', normal_center_border)
        sheet.write('V1', 'Sales Team', normal_center_border)
        sheet.write('W1', 'Due Date', normal_center_border)
        sheet.write('X1', 'Category', normal_center_border)
        sheet.write('Y1', 'Branch', normal_center_border)

        rows = 1
        number = 1
        
        state = False

        for value in sorted(pick_ids, key=lambda x: x['invoice']):

                if value[('sale')]=='0':
                    state='Offline'
                if value[('sale')]=='1':
                    state='TokoPedia'
                if value[('sale')]=='2':
                    state='Shopee'
                if value[('sale')]=='3':
                    state='Lazada'
                if value[('sale')]=='4':
                    state='Web'
                sheet.write('A'+str(rows+1), int(number), number_center)
                sheet.write('B'+str(rows+1), value[('dates')], date_format)
                sheet.write('C'+str(rows+1), value[str('partner_id')], normal_left_border)
                sheet.write('D'+str(rows+1), value[str('parent')], normal_left_border)
                sheet.write('E'+str(rows+1), state, normal_left_border)

                # sheet.write('E'+str(rows+1), value[str('tax_id')], normal_left_border)
                sheet.write('F'+str(rows+1), value[str('invoice_origin')], normal_left_border)
                sheet.write('G'+str(rows+1), value[('order_date')], date_format)
                sheet.write('H'+str(rows+1), value[str('picking')], number_center)
                sheet.write('I'+str(rows+1), value[('picking_date')], date_format)
                sheet.write('J'+str(rows+1), value[str('invoice')], number_center)
                sheet.write('K'+str(rows+1), value[str('refe')], number_center)
                # sheet.write('L'+str(rows+1), value[str('tax_id')], number_center)
                sheet.write('L'+str(rows+1), value[str('product_code')], number_center)
                sheet.write('M'+str(rows+1), value[str('product_id')], normal_left_border)
                sheet.write('N'+str(rows+1), value[str('uu')], normal_left_border)
                sheet.write('O'+str(rows+1), value[str('quantity')], normal_left_border)
                # sheet.write('N'+str(rows+1), value[str('volume')], normal_left_border)
                sheet.write('P'+str(rows+1), value[str('price_unit')], normal_left_border)
                sheet.write('Q'+str(rows+1), value[str('diskon')], normal_left_border)
                sheet.write('R'+str(rows+1), value[str('subtotal')], normal_left_border)
                sheet.write('S'+str(rows+1), value[str('payment_state')], normal_left_border)
                sheet.write('T'+str(rows+1), value[('date_create')], date_format)
                sheet.write('U'+str(rows+1), value[str('login')], normal_left_border)
                sheet.write('V'+str(rows+1), value[str('name')], normal_left_border)
                # sheet.write('Y'+str(rows+1), value[str('joko')], normal_left_border)
                sheet.write('W'+str(rows+1), value[('dates_due')], normal_left_border)
                sheet.write('X'+str(rows+1), value[('categ')], normal_left_border)
                # sheet.write('Y'+str(rows+1), value[('')], normal_left_border)
                state=False


                number +=1 
                rows += 1
                    


                    



        workbook.close()
        out = base64.encodestring(bz_data.getvalue())
        self.write({'data_binary': out, 'filename': filename})
        bz_data.close()
        action = {
            'name': 'Report Lead Time Vendor',
            'type': 'ir.actions.act_url',
            'url': 'web/content/?model=sale.wizard&id='+str(self.id)+\
                '&filename_field=filename&field=data_binary&download=true&filename='+filename,
            'target': 'self',
        }
        return action
        
