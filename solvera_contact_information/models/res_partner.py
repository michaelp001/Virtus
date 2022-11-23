
import datetime
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime,timedelta

class ResPartner(models.Model):
    _inherit = 'res.partner'
   
    state_sale = fields.Selection([
        ('0', 'Offline'),
        ('1', 'Tokopedia'),
        ('2', 'Shopee'),
        ('3', 'Lazada'),
        ('4', 'Web'),
        ], string='Sumber Penjualan', readonly=False, copy=False, default='0')