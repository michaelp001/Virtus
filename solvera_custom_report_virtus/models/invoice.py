from odoo import fields,models,api
from datetime import datetime,date,timedelta
from odoo.exceptions import UserError
from num2words import num2words

class CustomInvoiceModule(models.Model):
    _inherit = "account.move"

    terbilang = fields.Char(string="Terbilangs",compute='Terbilang')
    terbilang_koma = fields.Char(string="Terbilang",compute='terbilangs_koma')


    def Terbilang(self):
        amount_total = int(self.amount_total)
        for this in self:
            this.terbilang = num2words(amount_total, lang='id')+" rupiah"

    def terbilangs_koma(self):
        amount_total = self.amount_total
        for this in self:
            this.terbilang_koma = num2words(amount_total, lang='id')+" rupiah"