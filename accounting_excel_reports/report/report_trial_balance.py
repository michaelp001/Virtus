# -*- coding: utf-8 -*-
# License: Odoo Proprietary License v1.0

from odoo import models


class ReportTrialBalanceExcel(models.Model):
    _name = "report.accounting_excel_reports.report_trialbalance_excel"
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Report Trial Balance Excel'

    def generate_xlsx_report(self, workbook, data, obj):
        report_obj = self.env['report.accounting_pdf_reports.report_trialbalance']
        result = report_obj._get_report_values(obj, data)
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
                                       'bottom': True, 'top': True})
        format7 = workbook.add_format({'font_size': 10, 'align': 'right', 'bold': False, 'right': True, 'left': True,
                                       'bottom': True, 'top': True})

        sheet.set_row(0, 40)
        sheet.set_column(0, 4, 25)

        sheet.merge_range('A1:E1', "Trial Balance", format1)

        sheet.write('A3', 'Display Account', format4)
        if data['form']['display_account'] == 'movement':
            sheet.write('B3', 'With Movements', format6)
        elif data['form']['display_account'] == 'not_zero':
            sheet.write('B3', 'With balance is not equal to 0', format6)
        else:
            sheet.write('B3', 'All', format6)
        sheet.write('D3', 'Target Moves', format4)
        if data['form']['target_move'] == 'posted':
            sheet.write('E3', 'All Posted Entries', format6)
        else:
            sheet.write('E3', 'All Entries', format6)

        if data['form']['date_from']:
            sheet.write('A4', "Date From", format4)
            sheet.write('B4', data['form']['date_from'], format6)
        if data['form']['date_to']:
            sheet.write('D4', "Date To", format4)
            sheet.write('E4', data['form']['date_to'], format6)

        sheet.write('A6', "Code ", format2)
        sheet.write('B6', "Account", format2)
        sheet.write('C6', "Debit", format3)
        sheet.write('D6', "Credit", format3)
        sheet.write('E6', "Balance", format3)
        row = 6
        col = 0
        for account in result['Accounts']:
            sheet.write(row, col, account['code'], format6)
            sheet.write(row, col+1, account['name'], format6)
            sheet.write(row, col+2, account['debit'], format7)
            sheet.write(row, col+3, account['credit'], format7)
            sheet.write(row, col+4, account['balance'], format7)
            row += 1
