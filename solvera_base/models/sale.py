
import datetime
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime,timedelta

class SaleOrder(models.Model):
    _inherit = 'sale.order'
   
    address_inv = fields.Char(string="Delivery Detail",related="partner_invoice_id.street")
    address_del = fields.Char(string="Delivery Detail",related="partner_shipping_id.street")
    internal_name = fields.Char(string='Internal Name', related="partner_id.internal_name")


