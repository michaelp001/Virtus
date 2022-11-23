
import datetime
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import date, datetime,timedelta

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    Flag_tanggal_dikirim = fields.Date(string="Delivery Time")


    def delivery(self):
        today = date.today()
        res = super(StockPicking, self).delivery()
        print('cek_flag')
        self.Flag_tanggal_dikirim=today

        return res
            

    def delivery_part(self):
        today = date.today()
        res = super(StockPicking, self).delivery()
        self.Flag_tanggal_dikirim=today

        return res