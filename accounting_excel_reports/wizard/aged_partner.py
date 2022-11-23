# -*- coding: utf-8 -*-
# License: Odoo Proprietary License v1.0

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountAgedTrialBalance(models.TransientModel):
    _inherit = 'account.aged.trial.balance'

    def _print_report(self, data):
        if self._context.get('excel_report'):
            res = {}
            data = self.pre_print_report(data)
            data['form'].update(self.read(['period_length'])[0])
            period_length = data['form']['period_length']
            if period_length<=0:
                raise UserError(_('You must set a period length greater than 0.'))
            if not data['form']['date_from']:
                raise UserError(_('You must set a start date.'))

            start = data['form']['date_from']

            for i in range(5)[::-1]:
                stop = start - relativedelta(days=period_length - 1)
                res[str(i)] = {
                    'name': (i!=0 and (str((5-(i+1)) * period_length) + '-' + str((5-i) * period_length)) or ('+'+str(4 * period_length))),
                    'stop': start.strftime('%Y-%m-%d'),
                    'start': (i!=0 and stop.strftime('%Y-%m-%d') or False),
                }
                start = stop - relativedelta(days=1)
            data['form'].update(res)
            return self.env.ref('accounting_excel_reports.action_aged_partner_balance_excel').report_action(
                self, data=data)
        else:
            return super(AccountAgedTrialBalance, self)._print_report(data)
