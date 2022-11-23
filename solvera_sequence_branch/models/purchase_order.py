from odoo import fields,models,api
from datetime import datetime,date,timedelta
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_compare, float_round

class Purchaseorder(models.Model):
    _inherit = "purchase.order"

    @api.model
    def create(self, vals):
        print('asdasdasd')
        res = super(Purchaseorder,self).create(vals)
        for this in res:
            this.name = 'PO-'+str(this.partner_id.kode)+self.env['ir.sequence'].next_by_code('virtus.PO')
            print('laksmdlakmsdklm')
        return res