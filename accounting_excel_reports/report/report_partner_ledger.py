# -*- coding: utf-8 -*-
# License: Odoo Proprietary License v1.0

from odoo import models


class ReportPartnerLedgerExcel(models.Model):
    _name = "report.accounting_excel_reports.report_partnerledger_excel"
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Report Partner Ledger Excel'

    def generate_xlsx_report(self, workbook, data, obj):
        report_obj = self.env['report.accounting_pdf_reports.report_partnerledger']
        result = report_obj._get_report_values(obj, data)

        format1 = workbook.add_format({'font_size': 14, 'bottom': True, 'right': True, 'left': True, 'top': True,
                                       'align': 'center', 'bold': True, 'bg_color': '#bfbfbf', 'valign': 'vcenter'})
        format2 = workbook.add_format({'font_size': 12, 'align': 'left', 'right': True, 'left': True,
                                       'bottom': True, 'top': True, 'bold': True, 'bg_color': '#bfbfbf'})
        format3 = workbook.add_format({'font_size': 12, 'align': 'right', 'right': True, 'left': True,
                                       'bottom': True, 'top': True, 'bold': True, 'bg_color': '#bfbfbf'})
        format4 = workbook.add_format({'font_size': 10, 'align': 'left', 'bold': True, 'right': True, 'left': True,
                                       'bottom': True, 'top': True})
        format5 = workbook.add_format({'font_size': 10, 'align': 'right', 'bold': True, 'right': True, 'left': True,
                                       'bottom': True, 'top': True})
        format6 = workbook.add_format({'font_size': 10, 'align': 'left', 'bold': False, 'right': True, 'left': True,
                                       'bottom': True, 'top': True})
        format7 = workbook.add_format({'font_size': 10, 'align': 'right', 'bold': False, 'right': True, 'left': True,
                                       'bottom': True, 'top': True})
        format8 = workbook.add_format({'font_size': 10, 'align': 'left', 'bold': False, 'right': True, 'left': True,
                                       'bottom': True, 'top': True, 'num_format': 'yyyy-mm-dd'})

        sheet = workbook.add_worksheet()

        sheet.set_row(0, 40)
        sheet.set_column(0, 1, 13)
        sheet.set_column(2, 6, 25)

        sheet.merge_range('A1:G1', "Partner Ledger Report", format1)

        sheet.merge_range('A3:B3', "Company", format4)
        sheet.write('C3', data['form']['company_id'][1], format6)
        sheet.write('F3', 'Target Moves', format4)
        if data['form']['target_move'] == 'posted':
            sheet.write('G3', 'All Posted Entries', format6)
        else:
            sheet.write('G3', 'All Entries', format6)

        if data['form']['date_from']:
            sheet.merge_range('A4:B4', "Date From", format4)
            sheet.write('C4', data['form']['date_from'], format6)
        if data['form']['date_to']:
            sheet.write('F4', "Date To", format4)
            sheet.write('G4', data['form']['date_to'], format6)

        sheet.write('A6', "Date ", format2)
        sheet.write('B6', "JRNL", format2)
        sheet.write('C6', "Account", format2)
        sheet.write('D6', "Ref", format2)
        sheet.write('E6', "Debit", format3)
        sheet.write('F6', "Credit", format3)
        sheet.write('G6', "Balance", format3)

        row = 6
        col = 0

        for o in result['docs']:
            sheet.merge_range(row, col, row, col+3, o.ref or '' + '-' + o.name, format4)
            sheet.write(row, col+4, result['sum_partner'](result['data'], o, 'debit'), format5)
            sheet.write(row, col+5, result['sum_partner'](result['data'], o, 'credit'), format5)
            sheet.write(row, col+6, result['sum_partner'](result['data'], o, 'debit - credit'), format5)
            row += 1
            for line in result['lines'](result['data'], o):
                sheet.write(row, col, line['date'], format8)
                sheet.write(row, col + 1, line['code'], format6)
                sheet.write(row, col + 2, line['a_code'], format6)
                sheet.write(row, col + 3, line['displayed_name'] or '', format6)
                sheet.write(row, col + 4, line['debit'], format7)
                sheet.write(row, col + 5, line['credit'], format7)
                sheet.write(row, col + 6, line['progress'], format7)
                row += 1
