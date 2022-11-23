# -*- coding: utf-8 -*-
# License: Odoo Proprietary License v1.0

from odoo import fields, models, api, _


class AccountReportFinancial(models.TransientModel):
    _inherit = "accounting.report"

    def _print_report(self, data):
        if self._context.get('excel_report'):
            data['form'].update(self.read(
                ['date_from_cmp', 'debit_credit', 'date_to_cmp', 'filter_cmp', 'account_report_id', 'enable_filter',
                 'label_filter', 'target_move'])[0])
            return self.env.ref('accounting_excel_reports.action_report_financial_excel').report_action(
                self, data=data, config=False)
        else:
            return super(AccountReportFinancial, self)._print_report(data)
