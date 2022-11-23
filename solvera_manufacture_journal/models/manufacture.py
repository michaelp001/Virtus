
from datetime import datetime,timedelta
from shutil import move
from odoo import models, fields, api,_
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_is_zero

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def replace_account(self):
        for i in self:
            for line in i.move_finished_ids:
                for move in line.account_move_ids:
                    for acc in move.line_ids:
                        if acc.debit:
                            acc.with_context(check_move_validity=False).write({
                                'account_id':line.product_id.categ_id.property_account_input_production_categ_id.id,
                            })
                        if acc.credit:
                            acc.with_context(check_move_validity=False).write({
                                'account_id':line.product_id.categ_id.property_account_output_production_categ_id.id,
                            })
            for lines in i.move_raw_ids:
                for moves in lines.account_move_ids:
                    for accs in moves.line_ids:
                        if accs.debit:
                            accs.with_context(check_move_validity=False).write({
                                'account_id':lines.product_id.categ_id.property_account_output_production_categ_id.id,
                            })
                        if accs.credit:
                            accs.with_context(check_move_validity=False).write({
                                'account_id':lines.product_id.categ_id.property_account_input_production_categ_id.id,
                            })

    def button_mark_done(self):
        res=super(MrpProduction, self).button_mark_done()
        if self.qty_producing != 0:
            self.replace_account()

        return res