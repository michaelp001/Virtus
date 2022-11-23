
import datetime
import string
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime,timedelta

class SaleOrder(models.Model):
    _inherit = 'purchase.order.line'

    uom_description = fields.Char(related="product_uom.uom_description")
    ##permintaan UOM Description
    