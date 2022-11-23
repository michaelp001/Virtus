# -*- coding: utf-8 -*-
# License: Odoo Proprietary License v1.0

import time
from odoo import models


class ReportAgedPartnerBalanceExcel(models.Model):
    _name = "report.accounting_excel_reports.agedpartnerbalance_excel"
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Report Aged Partner Balance Excel'

    def generate_xlsx_report(self, workbook, data, obj):
        report_obj = self.env['report.accounting_pdf_reports.report_agedpartnerbalance']
        form_data = data['form']
        target_move = data['form'].get('target_move', 'all')
        date_from = data['form'].get('date_from', time.strftime('%Y-%m-%d'))
        if data['form']['result_selection'] == 'customer':
            account_type = ['receivable']
        elif data['form']['result_selection'] == 'supplier':
            account_type = ['payable']
        else:
            account_type = ['payable', 'receivable']
        movelines, total, dummy = report_obj._get_partner_move_lines(account_type, date_from, target_move,
                                                               data['form']['period_length'])
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
        sheet.set_column(0, 0, 30)
        sheet.set_column(1, 7, 15)

        sheet.merge_range('A1:H1', "Aged Partner Balance", format1)

        sheet.write('A3', "Partner's", format4)
        if data['form']['result_selection'] == 'customer':
            sheet.merge_range('B3:C3', 'Receivable Accounts', format6)
        elif data['form']['result_selection'] == 'supplier':
            sheet.merge_range('B3:C3', 'Payable Accounts', format6)
        else:
            sheet.merge_range('B3:C3', 'Receivable and Payable Accounts', format6)
        sheet.merge_range('E3:F3', 'Target Moves', format4)
        if data['form']['target_move'] == 'posted':
            sheet.merge_range('G3:H3', 'All Posted Entries', format6)
        else:
            sheet.merge_range('G3:H3', 'All Entries', format6)

        sheet.write('A4', "Period Length (days)", format4)
        sheet.merge_range('B4:C4', data['form']['period_length'], format6)
        if data['form']['date_from']:
            sheet.merge_range('E4:F4', "Date From", format4)
            sheet.merge_range('G4:H4', data['form']['date_from'], format6)

        sheet.write('A6', "Partners ", format2)
        sheet.write('B6', "Not due", format2)
        sheet.write('C6', form_data['4']['name'], format3)
        sheet.write('D6', form_data['3']['name'], format3)
        sheet.write('E6', form_data['2']['name'], format3)
        sheet.write('F6', form_data['1']['name'], format3)
        sheet.write('G6', form_data['0']['name'], format3)
        sheet.write('H6', "Total", format3)
        row = 6
        if movelines:
            col = 0
            sheet.write(row, col, "Account Total", format4)
            sheet.write(row, col+1, total[6], format5)
            sheet.write(row, col+2, total[4], format5)
            sheet.write(row, col+3, total[3], format5)
            sheet.write(row, col+4, total[2], format5)
            sheet.write(row, col+5, total[1], format5)
            sheet.write(row, col+6, total[0], format5)
            sheet.write(row, col+7, total[5], format5)
            row += 1
        for partner in movelines:
            col = 0
            sheet.write(row, col, partner['name'], format4)
            sheet.write(row, col + 1, partner['direction'], format7)
            sheet.write(row, col + 2, partner['4'], format7)
            sheet.write(row, col + 3, partner['3'], format7)
            sheet.write(row, col + 4, partner['2'], format7)
            sheet.write(row, col + 5, partner['1'], format7)
            sheet.write(row, col + 6, partner['0'], format7)
            sheet.write(row, col + 7, partner['total'], format7)
            row += 1
