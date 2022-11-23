# -*- coding: utf-8 -*-
# License: Odoo Proprietary License v1.0

from odoo import models, api


class AccountTaxReport(models.TransientModel):
    _inherit = 'account.tax.report.wizard'

    def _print_report(self, data):
        if self._context.get('excel_report'):
            return self.env.ref('accounting_excel_reports.action_report_account_tax_excel').report_action(
                self, data=data)
        else:
            return super(AccountTaxReport, self)._print_report(data)
