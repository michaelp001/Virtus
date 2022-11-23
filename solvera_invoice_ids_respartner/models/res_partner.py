
import datetime
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime,timedelta

class ResPartner(models.Model):
    _inherit = 'res.partner'

    invoice_ids = fields.One2many('account.move','partner_id')

   