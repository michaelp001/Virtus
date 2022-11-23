

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime,timedelta

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    tukar_faktur_allow = fields.Boolean(string='Tukar Faktur')