
import datetime
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime,timedelta

class StockPicking(models.Model):
    _inherit = 'account.move'

    faktur_pajak = fields.Char(string="Faktur Pajak")
    
