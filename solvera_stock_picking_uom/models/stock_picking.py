

from collections import defaultdict
from itertools import groupby
from operator import itemgetter
from re import findall as regex_findall
from re import split as regex_split
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime,timedelta



class stock_move(models.Model):
    _inherit = 'stock.move'

    uom_convert = fields.Float(string="Done UOM PO")
    uom_demand = fields.Float(string="Demand UOM PO",compute="compute_demand")
    uom_id_converter = fields.Many2one('uom.uom',string="UOM Purchase",related="product_id.uom_po_id")


    def compute_demand(self):
        for this in self:
            demand = this.product_uom_qty/this.product_id.uom_po_id.factor_inv
            this.uom_demand = demand

    @api.onchange('quantity_done')
    def compute_qty_convert(self):
        if self.uom_id_converter != self.product_uom:
            for this in self:
                    done = this.quantity_done / this.product_id.uom_po_id.factor_inv
                    this.uom_convert = done

class stock_move(models.Model):
    _inherit = 'stock.move.line'

    uom_convert = fields.Float(string="Done PO UOM")
    uom_id_converter = fields.Many2one('uom.uom',string="UOM Purchase",related="product_id.uom_po_id")
    picking_type_code = fields.Selection(
        related='picking_id.picking_type_code',
        readonly=True)
   
    @api.onchange('uom_convert')
    def done_convert(self):
        for this in self:
            if this.uom_id_converter != this.product_uom_id:
                done = this.uom_convert *this.product_id.uom_po_id.factor_inv
                this.qty_done = done


    @api.onchange('qty_done')
    def compute_qty_convert(self):
        for this in self:
            if this.uom_id_converter != this.product_uom_id:
                done = this.qty_done / this.product_id.uom_po_id.factor_inv
                this.uom_convert=done
