
import datetime
from unicodedata import category
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime,timedelta

class ResPartner(models.Model):
    _inherit = 'res.partner'
   
    kode = fields.Char(string='Kode')
    internal_name = fields.Char(string='Internal Name')
    category_state = fields.Selection([
    ('1', 'Sumber Dana'),
    ('2', 'Vendor'),
    ('3', 'Employee'),
    ], string='Category', readonly=False, copy=False,required=True)
    batasan_state = fields.Selection([
    ('1', 'tanpa pembatasan'),
    ('2', 'Dengan Pembatasan'),
    ], string='Batasan Sumbangan', readonly=False, copy=False,required=True)
    pernyataan_boolean = fields.Boolean(string="Mengakui L/R selisih kurs")