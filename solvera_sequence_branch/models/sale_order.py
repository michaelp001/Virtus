from odoo import fields,models,api
from datetime import datetime,date,timedelta
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_compare, float_round

class SaleOrder(models.Model):
    _inherit = "sale.order"

    state_sale = fields.Selection([
    ('0', 'Offline'),
    ('1', 'Tokopedia'),
    ('2', 'Shopee'),
    ('3', 'Lazada'),
    ('4', 'Web'),
    ], string='Sumber Penjualan', readonly=False, copy=False, related="partner_id.state_sale")


    @api.model
    def create(self, vals):
        res = super(SaleOrder,self).create(vals)
        for this in res:
            if this.state_sale == "0":
                if this.branch_id.id == 1:
                    this.name = self.env['ir.sequence'].next_by_code('branch.jakarta.virtus')
                elif this.branch_id.id == 2:
                    this.name = self.env['ir.sequence'].next_by_code('branch.surabaya.virtus')
                elif this.branch_id.id == 3:
                    this.name = self.env['ir.sequence'].next_by_code('branch.bali.virtus')

            if this.state_sale == "1":
                if this.branch_id.id == 1:
                    this.name = self.env['ir.sequence'].next_by_code('branch.jakarta.virtus.tp')
                elif this.branch_id.id == 2:
                    this.name = self.env['ir.sequence'].next_by_code('branch.surabaya.virtus.tp')
                elif this.branch_id.id == 3:
                    this.name = self.env['ir.sequence'].next_by_code('branch.bali.virtus.tp')

            if this.state_sale == "2":
                if this.branch_id.id == 1:
                    this.name = self.env['ir.sequence'].next_by_code('branch.jakarta.virtus.sp')
                elif this.branch_id.id == 2:
                    this.name = self.env['ir.sequence'].next_by_code('branch.surabaya.virtus.sp')
                elif this.branch_id.id == 3:
                    this.name = self.env['ir.sequence'].next_by_code('branch.bali.virtus.sp')

            if this.state_sale == "3":
                if this.branch_id.id == 1:
                    this.name = self.env['ir.sequence'].next_by_code('branch.jakarta.virtus.lz')
                elif this.branch_id.id == 2:
                    this.name = self.env['ir.sequence'].next_by_code('branch.surabaya.virtus.lz')
                elif this.branch_id.id == 3:
                    this.name = self.env['ir.sequence'].next_by_code('branch.bali.virtus.lz')
            
            if this.state_sale == "4":
                if this.branch_id.id == 1:
                    this.name = self.env['ir.sequence'].next_by_code('branch.jakarta.virtus.wb')
                elif this.branch_id.id == 2:
                    this.name = self.env['ir.sequence'].next_by_code('branch.surabaya.virtus.wb')
                elif this.branch_id.id == 3:
                    this.name = self.env['ir.sequence'].next_by_code('branch.bali.virtus.wb')
        return res