# -*- coding: utf-8 -*-
# License: Odoo Proprietary License v1.0

from odoo import fields, models, api, _


class AccountPartnerLedger(models.TransientModel):
    _inherit = "account.report.partner.ledger"

    def _print_report(self, data):
        if self._context.get('excel_report'):
            data = self.pre_print_report(data)
            data['form'].update({'reconciled': self.reconciled, 'amount_currency': self.amount_currency})
            return self.env.ref('accounting_excel_reports.action_report_partnerledger_excel').report_action(
                self, data=data)
        else:
            return super(AccountPartnerLedger, self)._print_report(data)
