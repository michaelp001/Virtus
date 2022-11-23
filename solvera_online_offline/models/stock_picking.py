from odoo import fields,models,api,_
from datetime import datetime,date,timedelta
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = "stock.picking"

    def change_source(self):
        for this in self:
           if this.state_sale != "0":
            wh_obj = self.env['stock.location'].search([('branch_id','=',this.partner_id.parent_id.branch_id.id ),('state_source','=','1')])
            if wh_obj:
                this.location_id=wh_obj
                # this.write({'location_id': wh_obj})
        
        

    
class StockLocation(models.Model):
    _inherit = 'stock.location'

    state_source = fields.Selection([
    ('0', 'Offline'),
    ('1', 'Online'),
    ], string='Sumber', readonly=False, copy=False)

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def write(self, vals):

        login = self.env.user.has_group('purchase.group_purchase_manager')
        print(login,'')
        if self.state== "purchase":
            if login == False:
                raise UserError(_("No edit in done state"))

        return super().write(vals)