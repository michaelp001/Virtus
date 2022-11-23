# -*- coding: utf-8 -*-
# License: Odoo Proprietary License v1.0

from odoo import fields, models, api


class AccountBalanceReport(models.TransientModel):
    _inherit = 'account.balance.report'

    def _print_report(self, data):
        if self._context.get('excel_report'):
            data = self.pre_print_report(data)
            records = self.env[data['model']].browse(data.get('ids', []))
            return self.env.ref('accounting_excel_reports.action_report_trial_balance_excel').report_action(
                records, data=data)
        else:
            return super(AccountBalanceReport, self)._print_report(data)
