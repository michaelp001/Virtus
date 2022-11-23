
from datetime import date
from shutil import move
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_is_zero

class stockmove(models.Model):
    _inherit = 'stock.picking'
    def valuation_journal(self):
        val_obj = self.env['stock.move'].search([])
        for i in val_obj:
            if i.picking_code=='internal':
                for line in i.account_move_ids:
                    for lines in line.line_ids:
                        if lines.account_id.id not in [1399,1494]:
                            if lines.account_id.id != i.product_id.categ_id.property_account_persediaan_transfer_jakarta_categ_id.id:
                                lines.write({
                                        'account_id': i.product_id.categ_id.property_account_persediaan_transfer_jakarta_categ_id.id
                                    })
                                # print(lines.account_id.name,'idnya',lines.account_id.id,'namanya',i.product_id.name)
    def perbaikan_journal_bodoh(self):
        account_obj = self.env['account.move'].search([('move_type','=','out_invoice')])
        for i in account_obj:
            for line in i.invoice_line_ids:
                if line.account_id.id == 1529 and line.account_id.id != line.product_id.categ_id.property_account_income_categ_id.id:
                    line.write({
                                        'account_id': line.product_id.categ_id.property_account_income_categ_id.id
                                    })
    def perbaikan_journal_valuation_bodoh(self):
        val_obj = self.env['stock.move'].search([])
        for i in val_obj:
            if i.picking_code=='outgoing':
                for line in i.account_move_ids:
                    for lines in line.line_ids:
                        if lines.account_id.id == 1420 and lines.account_id.id != i.product_id.categ_id.property_stock_valuation_account_id.id:
                            lines.write({
                                                'account_id': i.product_id.categ_id.property_stock_valuation_account_id.id
                                            })
    def perbaikan_journal_valuation_bodoh(self):
        val_obj = self.env['stock.move'].search([])
        for i in val_obj:
            if i.picking_code=='outgoing':
                for line in i.account_move_ids:
                    for lines in line.line_ids:
                        if lines.account_id.id == 1420 and lines.account_id.id != i.product_id.categ_id.property_stock_valuation_account_id.id:
                            lines.write({
                                                'account_id': i.product_id.categ_id.property_stock_valuation_account_id.id
                                            })
                