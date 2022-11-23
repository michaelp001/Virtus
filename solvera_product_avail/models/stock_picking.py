
import datetime
from traceback import print_last
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime,timedelta

# class ResPartner(models.Model):
#     _inherit = 'stock.picking'

#     available_qty_warehouse = fields.Float(string="Available QTY",readonly=True)

#     def compute_qty(self):
#         for i in self:
#             for line in i.move_ids_without_package:
#                 qty = line.product_id.qty_available
#                 i.available_qty_warehouse =qty


class stockmoveline(models.Model):
    _inherit = 'stock.move.line'

    available_qty_warehouse = fields.Float(string="Available QTY")

    @api.onchange('product_id')
    def compute_qty(self):
        quant_obj = self.env['stock.location'].search([('id','=',self.location_id.id)])
        for this in self:
            for line in quant_obj.quant_ids:
                if this.product_id.id == line.product_id.id:
                    this.available_qty_warehouse = line.available_quantity
                    # this.write({'available_qty_warehouse': line.available_quantity})
    
