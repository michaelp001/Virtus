# -*- coding: utf-8 -*-
# License: Odoo Proprietary License v1.0

from odoo import models


class ReportGeneralLedgerExcel(models.Model):
    _name = "report.accounting_excel_reports.report_generalledger_excel"
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Report General Ledger Excel'

    def generate_xlsx_report(self, workbook, data, obj):
        report_obj = self.env['report.accounting_pdf_reports.report_general_ledger']
        results = report_obj._get_report_values(obj, data)
        sheet = workbook.add_worksheet()

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
                                       'bottom': True, 'top': True, 'text_wrap':'true'})
        format7 = workbook.add_format({'font_size': 10, 'align': 'right', 'bold': False, 'right': True, 'left': True,
                                       'bottom': True, 'top': True})
        format8 = workbook.add_format({'font_size': 10, 'align': 'left', 'bold': False, 'right': True, 'left': True,
                                       'bottom': True, 'top': True, 'num_format': 'yyyy-mm-dd'})

        sheet.set_row(0, 40)
        sheet.set_row(2, 40)
        sheet.set_column(0, 1, 13)
        sheet.set_column(2, 5, 25)
        sheet.set_column(6, 8, 15)

        sheet.merge_range('A1:I1', "General Ledger Report", format1)

        sheet.merge_range('A3:B3', "Journals", format4)
        sheet.write('C3', ', '.join([lt or '' for lt in results['print_journal']]), format6)
        sheet.write('G3', 'Target Moves', format4)
        if data['form']['target_move'] == 'posted':
            sheet.merge_range('H3:I3', 'All Posted Entries', format6)
        else:
            sheet.write('H3:I3', 'All Entries', format6)

        sheet.merge_range('A4:B4', "Display Account", format4)
        if data['form']['display_account'] == 'all':
            sheet.write('C4', 'All', format6)
        elif data['form']['display_account'] == 'movement':
            sheet.write('C4', 'With Movements', format6)
        else:
            sheet.write('C4', 'With balance is not equal to 0', format6)
        sheet.write('G4', 'Sorted By', format4)
        if data['form']['sortby'] == 'sort_date':
            sheet.merge_range('H4:I4', 'Date', format6)
        else:
            sheet.write('H4:I4', 'Journal & Partner', format6)

        if data['form']['date_from']:
            sheet.merge_range('A5:B5', "Date From", format4)
            sheet.write('C5', data['form']['date_from'], format6)
        if data['form']['date_to']:
            sheet.write('G5', "Date To", format4)
            sheet.merge_range('H5:I5', data['form']['date_to'], format6)

        sheet.write('A7', "Date ", format2)
        sheet.write('B7', "JRNL", format2)
        sheet.write('C7', "Partner", format2)
        sheet.write('D7', "Ref", format2)
        sheet.write('E7', "Move", format2)
        sheet.write('F7', "Entry Label", format2)
        sheet.write('G7', "Debit", format3)
        sheet.write('H7', "Credit", format3)
        sheet.write('I7', "Balance", format3)
        row = 7
        col = 0
        for account in results['Accounts']:
            sheet.merge_range(row, col, row, col + 5, account['code'] + account['name'], format4)
            sheet.write(row, col + 6, account['debit'], format5)
            sheet.write(row, col + 7, account['credit'], format5)
            sheet.write(row, col + 8, account['balance'], format5)
            for line in account['move_lines']:
                col = 0
                row += 1
                sheet.write(row, col, line['ldate'], format8)
                sheet.write(row, col + 1, line['lcode'], format6)
                sheet.write(row, col + 2, line['partner_name'], format6)
                sheet.write(row, col + 3, line['lref'] or '', format6)
                sheet.write(row, col + 4, line['move_name'], format6)
                sheet.write(row, col + 5, line['lname'], format6)
                sheet.write(row, col + 6, line['debit'], format7)
                sheet.write(row, col + 7, line['credit'], format7)
                sheet.write(row, col + 8, line['balance'], format7)
            row += 1
