# -*- coding: utf-8 -*-
# License: Odoo Proprietary License v1.0

from odoo import models


class ReportTaxExcel(models.Model):
    _name = "report.accounting_excel_reports.report_tax_excel"
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Report Tax Excel'

    def generate_xlsx_report(self, workbook, data, obj):
        report_obj = self.env['report.accounting_pdf_reports.report_tax']
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
        sheet.set_column(0, 0, 30)
        sheet.set_column(1, 2, 25)

        sheet.merge_range('A1:C1', "Tax Report", format1)

        sheet.write('A3', "Date From", format4)
        sheet.write('B3', result['data']['date_from'], format6)
        sheet.write('A4', "Date To", format4)
        sheet.write('B4', result['data']['date_to'], format6)
        sheet.write('A5', "Company", format4)
        sheet.write('B5', data['form']['company_id'][1], format6)

        sheet.write('A7', "", format3)
        sheet.write('B7', "Net", format3)
        sheet.write('C7', "Tax", format3)
        sheet.merge_range('A8:C8', "Sale", format4)
        row = 8
        col = 0
        for line in result['lines']['sale']:
            sheet.write(row, col, line.get('name'), format6)
            sheet.write(row, col+1, line.get('net'), format7)
            sheet.write(row, col+2, line.get('tax'), format7)
            row += 1
        sheet.merge_range(row, col, row, col+2, "Purchase", format4)
        row += 1
        for line in result['lines']['purchase']:
            sheet.write(row, col, line.get('name'), format6)
            sheet.write(row, col+1, line.get('net'), format7)
            sheet.write(row, col+2, line.get('tax'), format7)
            row += 1
