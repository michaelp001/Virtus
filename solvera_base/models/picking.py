
import datetime
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime,timedelta

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    address_del = fields.Char(Sting="Delivery Detail",related="partner_id.street")