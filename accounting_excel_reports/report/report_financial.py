# -*- coding: utf-8 -*-
# License: Odoo Proprietary License v1.0

from odoo import models


class ReportFinancialExcel(models.Model):
    _name = "report.accounting_excel_reports.report_financial_excel"
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Report Financial Excel'

    def generate_xlsx_report(self, workbook, data, obj):
        report_obj = self.env['report.accounting_pdf_reports.report_financial']
        report_lines = report_obj.get_account_lines(data.get('form'))
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
        sheet.set_column(0, 3, 25)

        sheet.merge_range('A1:D1', data['form']['account_report_id'][1], format1)

        sheet.write('A3', "Target Moves", format4)
        if data['form']['target_move'] == 'posted':
            sheet.write('B3', "All Posted Entries", format6)
        else:
            sheet.write('B3', "All Entries", format6)

        if data['form']['date_from'] and data['form']['date_to']:
            sheet.write('A4', "Date From", format4)
            sheet.write('B4', data['form']['date_from'], format6)
            sheet.write('A5', "Date To", format4)
            sheet.write('B5', data['form']['date_to'], format6)
            row = 6
        elif data['form']['date_from']:
            sheet.write('A4', "Date From", format4)
            sheet.write('B4', data['form']['date_from'], format6)
            row = 5
        elif data['form']['date_to']:
            sheet.write('A4', "Date To", format4)
            sheet.write('B4', data['form']['date_to'], format6)
            row = 5
        else:
            row = 4
        col = 0
        if data['form']['debit_credit'] == 1:
            sheet.write(row, col, "Name", format2)
            sheet.write(row, col+1, "Debit", format3)
            sheet.write(row, col+2, "Credit", format3)
            sheet.write(row, col+3, "Balance", format3)
            row += 1
            for line in report_lines:
                if line['level'] != 0:
                    if int(line['level']) > 3:
                        sheet.write(row, col, '  ' * int(line['level']) + line.get('name'), format6)
                        sheet.write(row, col+1, line.get('debit'), format7)
                        sheet.write(row, col+2, line.get('credit'), format7)
                        sheet.write(row, col+3, line.get('balance'), format7)
                    else:
                        sheet.write(row, col, '  ' * int(line['level']) + line.get('name'), format4)
                        sheet.write(row, col + 1, line.get('debit'), format5)
                        sheet.write(row, col + 2, line.get('credit'), format5)
                        sheet.write(row, col + 3, line.get('balance'), format5)
                    row += 1
        elif not data['form']['enable_filter'] and not data['form']['debit_credit']:
            sheet.merge_range(row, col, row, col+1, "Name", format2)
            sheet.merge_range(row, col+2, row, col+3, "Balance", format3)
            row += 1
            for line in report_lines:
                if line['level'] != 0:
                    if int(line['level']) > 3:
                        sheet.merge_range(row, col, row, col+1, '  ' * int(line['level']) + line.get('name'), format6)
                        sheet.merge_range(row, col+2, row, col+3, line.get('balance'), format7)
                    else:
                        sheet.merge_range(row, col, row, col + 1, '  ' * int(line['level']) + line.get('name'), format4)
                        sheet.merge_range(row, col + 2, row, col + 3, line.get('balance'), format5)
                    row += 1
        elif data['form']['enable_filter'] == 1 and not data['form']['debit_credit']:
            sheet.merge_range(row, col, row, col+1, "Name", format2)
            sheet.write(row, col+2, "Balance", format3)
            sheet.write(row, col+3, data['form']['label_filter'], format2)
            row += 1
            for line in report_lines:
                if line['level'] != 0:
                    if int(line['level']) > 3:
                        sheet.merge_range(row, col, row, col+1, '  ' + line.get('name'), format6)
                        sheet.write(row, col+2, line.get('balance'), format7)
                        sheet.write(row, col+3, line.get('balance_cmp'), format7)
                    else:
                        sheet.merge_range(row, col, row, col + 1, '  ' + line.get('name'), format4)
                        sheet.write(row, col + 2, line.get('balance'), format5)
                        sheet.write(row, col + 3, line.get('balance_cmp'), format5)
                    row += 1
