
from datetime import date
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_is_zero

class accountmove(models.Model):
    _inherit = 'account.move'
   
    def perbaikan_asset(self):
        move_obj = self.env['account.move'].search([('asset_depreciation_ids',"!=",False),('move_type','=','entry')])
        dates  = date(2022, 8, 1)

        for this in move_obj:
            if this.date < dates:
                this.button_draft()
                this.button_cancel()
