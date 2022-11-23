
import datetime
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime,timedelta

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
   
    internal_name = fields.Char(string='Internal Name', related="partner_id.internal_name")