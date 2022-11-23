
import datetime
import string
from odoo import models, fields, api,_
from dateutil.relativedelta import relativedelta
from datetime import datetime,timedelta
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order.line'

    uom_description = fields.Char(related="product_uom.uom_description")
    fix_discount= fields.Float('Fix Discount')
    is_fix_discount=fields.Boolean('Fix Discount')

  