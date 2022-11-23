
import datetime
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime,timedelta


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all', tracking=5, digits='idr')
    amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_all',digits='idr')
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all', tracking=4,digits='idr')
   

class SaleOrderline(models.Model):
    _inherit = 'sale.order.line'


    price_unit = fields.Float('Unit Price', required=True, digits='Product Price', default=0.0)
    price_subtotal = fields.Float(compute='_compute_amount', string='Subtotal', readonly=True, store=True)
   



