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
    _name = 'journal.wizard'

    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date to')
    invoice_line_ids = fields.Many2many('account.move')
    filename = fields.Char(size=256, readonly=True)
    data_binary = fields.Binary('Content Data', readonly=True)
    # salesperson = fields.Many2one('res.users')


    def export_faktur_excel(self):


        query = """
        SELECT	TO_CHAR(am.invoice_date, 'DD/MM/YYYY') as dates ,TO_CHAR(am.invoice_date, 'YYYY') as year, am.name as invoice, rp.name as partner_id,
            ptemp.name as product_id, ptemp.default_code as product_code ,
            round(aml.price_unit,0) as price_unit, round(aml.discount,0), round(aml.quantity,0) as quantity,am.state, am.payment_state,
            am.move_type,REPLACE(REPLACE (rp.vat, '-', ''), '.', '') as npwp, rp.kode, round(am.amount_total,0), round(am.amount_tax,0) as ppn
			,round(am.amount_total+am.amount_tax) as total, round(aml.price_subtotal,0) as subtotal,round(aml.price_subtotal * 0.11,0) as ppn11,
			round(aml.price_unit*aml.quantity-aml.price_subtotal,0) as diskon, round(am.amount_untaxed,0) as untax, round(am.amount_untaxed * 0.11) as untax11
			,REPLACE(REPLACE (rp.vat, '-', ''), '.', '') as tax_id, am.payment_reference as refe,  aml.account_id as account, REPLACE (REPLACE (SUBSTRING(am.faktur_pajak, 4, 100), '.', ''), '-', '') as pajak
            ,aml.id, rp.street as street ,TO_CHAR(am.invoice_date, 'MM') as month
        FROM account_move_line aml
            JOIN account_move am on aml.move_id =am.id
            LEFT JOIN res_partner rp on am.partner_id = rp.id
            LEFT JOIN product_product product on aml.product_id = product.id
            LEFT JOIN product_template ptemp on product.product_tmpl_id = ptemp.id
        WHERE am.move_type = 'out_invoice' AND am.state != 'cancel' and aml.product_id is not null and aml.price_unit > 0 and aml.picking is not null and am.invoice_date >= %s AND am.invoice_date <= %s 
        ORDER BY am.name asc, aml.id asc;
        """
        params = (self.date_from, self.date_to,)
        self.env.cr.execute(query,params)
        pick_ids = self.env.cr.dictfetchall()

 
        bz_data = io.BytesIO()
        workbook = xlsxwriter.Workbook(bz_data)
        filename = 'E-faktur.xls'
        
        sheet = workbook.add_worksheet('Journal')
        sheet.set_column('A:A', 17)
        sheet.set_column('B:B', 15)
        sheet.set_column('C:C', 35)
        sheet.set_column('D:D', 30)
        sheet.set_column('E:E', 50)
        sheet.set_column('F:F', 17)
        sheet.set_column('G:G', 20)
        sheet.set_column('H:H', 15)
        sheet.set_column('I:I', 50)
        sheet.set_column('J:J', 5)
        sheet.set_column('K:K', 10)
        sheet.set_column('L:L', 10)
        sheet.set_column('M:M', 10)
        sheet.set_column('N:N', 10)
        sheet.set_column('O:O', 10)
        sheet.set_column('P:P', 10)
        sheet.set_column('Q:Q', 10)
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
        sheet.write('A1', 'FK', normal_left)
        sheet.write('A2', 'LT', normal_left)
        sheet.write('A3', 'OF', normal_left)
        sheet.write('B1', 'KD_JENIS_TRANSAKSI', normal_left)
        sheet.write('B2', 'NPWP', normal_left)
        sheet.write('B3', 'KODE_OBJEK', normal_left)
        sheet.write('C1', 'FG_PENGGANTI', normal_left)
        sheet.write('C2', 'NAMA', normal_left)
        sheet.write('C3', 'NAMA', normal_left)
        sheet.write('D1', 'NOMOR_FAKTUR', normal_left)
        sheet.write('D2', 'JALAN', normal_left)
        sheet.write('D3', 'HARGA_SATUAN', normal_left)
        sheet.write('E1', 'MASA_PAJAK', normal_left)
        sheet.write('E2', 'BLOK', normal_left)
        sheet.write('E3', 'JUMLAH_BARANG', normal_left)
        sheet.write('F1', 'TAHUN_PAJAK', normal_left)
        sheet.write('F2', 'NOMOR', normal_left)
        sheet.write('F3', 'HARGA_TOTAL', normal_left)
        sheet.write('G1', 'TANGGAL_FAKTUR', normal_left)
        sheet.write('G2', 'RT', normal_left)
        sheet.write('G3', 'DISKON', normal_left)
        sheet.write('H1', 'NPWP', normal_left)
        sheet.write('H2', 'RW', normal_left)
        sheet.write('H3', 'DPP', normal_left)
        sheet.write('I1', 'NAMA', normal_left)
        sheet.write('I2', 'KECAMATAN', normal_left)
        sheet.write('I3', 'PPN', normal_left)
        sheet.write('J1', 'ALAMAT_LENGKAP', normal_left)
        sheet.write('J2', 'KELURAHAN', normal_left)
        sheet.write('J3', 'TARIF_PPNBM', normal_left)
        sheet.write('K1', 'JUMLAH_DPP', normal_left)
        sheet.write('K2', 'KABUPATEN', normal_left)
        sheet.write('K3', 'PPNBM', normal_left)
        sheet.write('L1', 'JUMLAH_PPN', normal_left)
        sheet.write('L2', 'PROPINSI', normal_left)
        sheet.write('M1', 'JUMLAH_PPNBM', normal_left)
        sheet.write('M2', 'KODE_POS', normal_left)
        sheet.write('N1', 'ID_KETERANGAN_TAMBAHAN', normal_left)
        sheet.write('N2', 'NOMOR_TELEPON', normal_left)
        sheet.write('O1', 'FG_UANG_MUKA', normal_left)
        sheet.write('P1', 'UANG_MUKA_DPP', normal_left)
        sheet.write('Q1', 'UANG_MUKA_PPN', normal_left)
        sheet.write('R1', 'UANG_MUKA_PPNBM', normal_left)
        sheet.write('S1', 'REFERENSI', normal_left)
        sheet.write('T1', 'KODE_DOKUMEN_PENDUKUNG', normal_left)

        rows = 3
        rows2 = 5
        number = 1
        invoice_temp =False
        partner_temp = False
  
        if pick_ids:
            for value in pick_ids:
                if value['invoice'] == invoice_temp :
                    sheet.write('A'+str(rows+1), 'OF', normal_left_border)
                    sheet.write('C'+str(rows+1), value[str('product_id')], normal_left_border)
                    sheet.write('D'+str(rows+1), value[('price_unit')], normal_left_border)
                    sheet.write('E'+str(rows+1), value[('quantity')], normal_left_border)
                    sheet.write('F'+str(rows+1), value[('subtotal')], number_center)
                    sheet.write('G'+str(rows+1), value[('diskon')], number_center)
                    sheet.write('H'+str(rows+1), value[('subtotal')], number_center)
                    sheet.write('I'+str(rows+1), value[('ppn11')], normal_left_border)
                    sheet.write('J'+str(rows+1), '0', normal_left_border)
                    sheet.write('K'+str(rows+1), '0', normal_left_border)
                    # sheet.write('L'+str(rows+1), '0', normal_left_border)
                    sheet.write('M'+str(rows+1), '0', normal_left_border)
                    sheet.write('O'+str(rows+1), '0', normal_left_border)
                    sheet.write('P'+str(rows+1), '0', normal_left_border)
                    sheet.write('Q'+str(rows+1), '0', normal_left_border)
                    sheet.write('R'+str(rows+1), '0', normal_left_border)
                    
                   
                    rows=rows+1
                    invoice_temp = value['invoice']
                    partner_temp = value['partner_id']
                elif value['invoice'] != invoice_temp:
                    sheet.write('A'+str(rows+1), 'FK', normal_left_border)
                    sheet.write('B'+str(rows+1), '01', normal_left_border)
                    sheet.write('C'+str(rows+1), '0', normal_left_border)
                    sheet.write('D'+str(rows+1), value[str('pajak')], normal_left_border)
                    sheet.write('E'+str(rows+1), value[str('month')], normal_left_border)
                    ##bulan invoice
                    sheet.write('F'+str(rows+1), value[str('year')], number_center)
                    sheet.write('G'+str(rows+1), value[str('dates')], number_center)
                    sheet.write('H'+str(rows+1), value[str('tax_id')], number_center)
                    sheet.write('I'+str(rows+1), value[str('partner_id')], normal_left_border)
                    sheet.write('J'+str(rows+1), value[str('street')], normal_left_border)
                    sheet.write('K'+str(rows+1), value[str('untax')], normal_left_border)
                    sheet.write('L'+str(rows+1), value[str('untax11')], normal_left_border)
                    sheet.write('M'+str(rows+1), '0', normal_left_border)
                    sheet.write('O'+str(rows+1), '0', normal_left_border)
                    sheet.write('P'+str(rows+1), '0', normal_left_border)
                    sheet.write('Q'+str(rows+1), '0', normal_left_border)
                    sheet.write('R'+str(rows+1), '0', normal_left_border)
                    sheet.write('S'+str(rows+1), value[str('invoice')], normal_left_border)

                    sheet.write('A'+str(rows+2), 'OF', normal_left_border)
                    # sheet.write('B'+str(rows+2), '01', normal_left_border)
                    sheet.write('C'+str(rows+2), value[str('product_id')], normal_left_border)
                    sheet.write('D'+str(rows+2), value[str('price_unit')], normal_left_border)
                    sheet.write('E'+str(rows+2), value[str('quantity')], normal_left_border)
                    sheet.write('F'+str(rows+2), value[str('subtotal')], number_center)
                    sheet.write('G'+str(rows+2), value[str('diskon')], number_center)
                    sheet.write('H'+str(rows+2), value[str('subtotal')], number_center)
                    sheet.write('I'+str(rows+2), value[str('ppn11')], normal_left_border)
                    sheet.write('J'+str(rows+2), '0', normal_left_border)
                    sheet.write('K'+str(rows+2), '0', normal_left_border)
                    # sheet.write('L'+str(rows+2), value[str('ppn')], normal_left_border)
                    sheet.write('M'+str(rows+2), '0', normal_left_border)
                    sheet.write('O'+str(rows+2), '0', normal_left_border)
                    sheet.write('P'+str(rows+2), '0', normal_left_border)
                    sheet.write('Q'+str(rows+2), '0', normal_left_border)
                    sheet.write('R'+str(rows+2), '0', normal_left_border)
                    # sheet.write('S'+str(rows+2), value[str('invoice')], normal_left_border)
                    invoice_temp = value['invoice']
                    partner_temp = value['partner_id']
                    number +=1 
                    rows += 2
                    rows2 += 1
                    
                    



        workbook.close()
        out = base64.encodestring(bz_data.getvalue())
        self.write({'data_binary': out, 'filename': filename})
        bz_data.close()
        action = {
            'name': 'Report Lead Time Vendor',
            'type': 'ir.actions.act_url',
            'url': 'web/content/?model=journal.wizard&id='+str(self.id)+\
                '&filename_field=filename&field=data_binary&download=true&filename='+filename,
            'target': 'self',
        }
        return action


   