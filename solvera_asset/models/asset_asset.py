
import datetime
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime,timedelta
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_is_zero

class Assetasset(models.Model):
    _inherit = 'account.asset.asset'
    date_collection = fields.Datetime(string="Date Collection",readonly=False)
    
   