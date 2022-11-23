
import datetime
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime,timedelta
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _default_validity_date(self):
        if self.env['ir.config_parameter'].sudo().get_param('sale.use_quotation_validity_days'):
            days = int(self.env['ir.config_parameter'].sudo().get_param('sale.use_quotation_validity_days'))
            if days > 0:
                return fields.Date.to_string(datetime.now() + timedelta(days))
        return False

    validity_date = fields.Date(string='Expiration', readonly=True, copy=False, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
                            default=_default_validity_date)

    

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
   
    @api.onchange("price_unit")
    def limitation(self):
        for this in self:
            if this.price_unit < this.product_id.lst_price:
                item = this.product_id.lst_price
                msg = 'Minimum Price Is Rp.%s' % (item)
                raise UserError(('Input price is to low,  '
                                    'please fill price more than minimum. ' + msg))
