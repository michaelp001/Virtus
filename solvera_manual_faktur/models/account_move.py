
import datetime
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime,timedelta

class StockPicking(models.Model):
    _inherit = 'account.move'

    faktur_pajak = fields.Char(string="Faktur Pajak")
    state_sale = fields.Selection([
    ('0', 'Offline'),
    ('1', 'Tokopedia'),
    ('2', 'Shopee'),
    ('3', 'Lazada'),
    ('4', 'Web'),
    ], string='Sumber Penjualan', readonly=False, copy=False, related="invoice_line_ids.state_sale")
    
