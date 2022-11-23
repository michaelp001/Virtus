from odoo import fields,models,api
from datetime import datetime,date,timedelta
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = "stock.picking"
    location_id = fields.Many2one(
        'stock.location', "Source Location",
        default=lambda self: self.env['stock.picking.type'].browse(self._context.get('default_picking_type_id')).default_location_src_id,
        check_company=True, readonly=True, required=True,
        states={'draft': [('readonly', False)],'assigned': [('readonly', False)],'confirmed': [('readonly', False)]})

    state_sale = fields.Selection([
        ('0', 'Offline'),
        ('1', 'Tokopedia'),
        ('2', 'Shopee'),
        ('3', 'Lazada'),
        ('4', 'Web'),
        ], string='Sumber Penjualan',related='partner_id.state_sale')

    @api.model
    def create(self, vals):
        res = super(StockPicking,self).create(vals)
        for this in res:
            if this.picking_type_code == "outgoing":
                if this.state_sale == "0":
                    if this.partner_id.parent_id:
                        if this.partner_id.parent_id.branch_id.id == 1:
                            names = self.env['ir.sequence'].next_by_code('branch.jakarta.virtus.do')
                            this.name = names
                        elif this.partner_id.parent_id.branch_id.id == 2:
                            names = self.env['ir.sequence'].next_by_code('branch.surabaya.virtus.do')
                            this.name = names
                        elif this.partner_id.parent_id.branch_id.id == 3:
                            names = self.env['ir.sequence'].next_by_code('branch.bali.virtus.do')
                            this.name = names
                        else:
                            names = self.env['ir.sequence'].next_by_code('branch.jakarta.virtus.do')
                            this.name = names
                    else:
                        if this.partner_id.branch_id.id == 1:
                            names = self.env['ir.sequence'].next_by_code('branch.jakarta.virtus.do')
                            this.name = names
                        elif this.partner_id.branch_id.id == 2:
                            names = self.env['ir.sequence'].next_by_code('branch.surabaya.virtus.do')
                            this.name = names
                        elif this.partner_id.branch_id.id == 3:
                            names = self.env['ir.sequence'].next_by_code('branch.bali.virtus.do')
                            this.name = names
                        else:
                            names = self.env['ir.sequence'].next_by_code('branch.jakarta.virtus.do')
                            this.name = names
                    

                elif this.state_sale == "1":
                    if this.partner_id.parent_id:
                        if this.partner_id.parent_id.branch_id.id == 1:
                            names = self.env['ir.sequence'].next_by_code('branch.jakarta.virtus.tp.do')
                            this.name = names
                        elif this.partner_id.parent_id.branch_id.id == 2:
                            names = self.env['ir.sequence'].next_by_code('branch.surabaya.virtus.tp.do')
                            this.name = names
                        elif this.partner_id.parent_id.branch_id.id == 3:
                            names = self.env['ir.sequence'].next_by_code('branch.bali.virtus.tp.do')
                            this.name = names
                        else:
                            names = self.env['ir.sequence'].next_by_code('branch.jakarta.virtus.tp.do')
                            this.name = names
                    else:
                        if this.partner_id.branch_id.id == 1:
                            names = self.env['ir.sequence'].next_by_code('branch.jakarta.virtus.tp.do')
                            this.name = names
                        elif this.partner_id.branch_id.id == 2:
                            names = self.env['ir.sequence'].next_by_code('branch.surabaya.virtus.tp.do')
                            this.name = names
                        elif this.partner_id.branch_id.id == 3:
                            names = self.env['ir.sequence'].next_by_code('branch.bali.virtus.tp.do')
                            this.name = names
                        else:
                            names = self.env['ir.sequence'].next_by_code('branch.jakarta.virtus.tp.do')
                            this.name = names

                elif this.state_sale == "2":
                    if this.partner_id.parent_id:
                        if this.partner_id.parent_id.branch_id.id == 1:
                            names = self.env['ir.sequence'].next_by_code('branch.jakarta.virtus.sp.do')
                            this.name = names
                        elif this.partner_id.parent_id.branch_id.id == 2:
                            names = self.env['ir.sequence'].next_by_code('branch.surabaya.virtus.sp.do')
                            this.name = names
                        elif this.partner_id.parent_id.branch_id.id == 3:
                            names = self.env['ir.sequence'].next_by_code('branch.bali.virtus.sp.do')
                            this.name = names
                        else:
                            names = self.env['ir.sequence'].next_by_code('branch.jakarta.virtus.sp.do')
                            this.name = names
                    else:
                        if this.partner_id.branch_id.id == 1:
                            names = self.env['ir.sequence'].next_by_code('branch.jakarta.virtus.sp.do')
                            this.name = names
                        elif this.partner_id.branch_id.id == 2:
                            names = self.env['ir.sequence'].next_by_code('branch.surabaya.virtus.sp.do')
                            this.name = names
                        elif this.partner_id.branch_id.id == 3:
                            names = self.env['ir.sequence'].next_by_code('branch.bali.virtus.sp.do')
                            this.name = names
                        else:
                            names = self.env['ir.sequence'].next_by_code('branch.jakarta.virtus.sp.do')
                            this.name = names


                elif this.state_sale == "3":
                    if this.parent_id:
                       if this.partner_id.parent_id:
                        if this.partner_id.parent_id.branch_id.id == 1:
                            names = self.env['ir.sequence'].next_by_code('branch.jakarta.virtus.lz.do')
                            this.name = names
                        elif this.partner_id.parent_id.branch_id.id == 2:
                            names = self.env['ir.sequence'].next_by_code('branch.surabaya.virtus.lz.do')
                            this.name = names
                        elif this.partner_id.parent_id.branch_id.id == 3:
                            names = self.env['ir.sequence'].next_by_code('branch.bali.virtus.lz.do')
                            this.name = names
                        else:
                            names = self.env['ir.sequence'].next_by_code('branch.jakarta.virtus.lz.do')
                            this.name = names
                    else:
                        if this.partner_id.branch_id.id == 1:
                            names = self.env['ir.sequence'].next_by_code('branch.jakarta.virtus.lz.do')
                            this.name = names
                        elif this.partner_id.branch_id.id == 2:
                            names = self.env['ir.sequence'].next_by_code('branch.surabaya.virtus.lz.do')
                            this.name = names
                        elif this.partner_id.branch_id.id == 3:
                            names = self.env['ir.sequence'].next_by_code('branch.bali.virtus.lz.do')
                            this.name = names
                        else:
                            names = self.env['ir.sequence'].next_by_code('branch.jakarta.virtus.lz.do')
                            this.name = names
                        

                elif this.state_sale == "4":
                    if this.parent_id:
                       if this.partner_id.parent_id:
                        if this.partner_id.parent_id.branch_id.id == 1:
                            names = self.env['ir.sequence'].next_by_code('branch.jakarta.virtus.wb.do')
                            this.name = names
                        elif this.partner_id.parent_id.branch_id.id == 2:
                            names = self.env['ir.sequence'].next_by_code('branch.surabaya.virtus.wb.do')
                            this.name = names
                        elif this.partner_id.parent_id.branch_id.id == 3:
                            names = self.env['ir.sequence'].next_by_code('branch.bali.virtus.wb.do')
                            this.name = names
                        else:
                            names = self.env['ir.sequence'].next_by_code('branch.jakarta.virtus.wb.do')
                            this.name = names
                    else:
                        if this.partner_id.branch_id.id == 1:
                            names = self.env['ir.sequence'].next_by_code('branch.jakarta.virtus.wb.do')
                            this.name = names
                        elif this.partner_id.branch_id.id == 2:
                            names = self.env['ir.sequence'].next_by_code('branch.surabaya.virtus.wb.do')
                            this.name = names
                        elif this.partner_id.branch_id.id == 3:
                            names = self.env['ir.sequence'].next_by_code('branch.bali.virtus.wb.do')
                            this.name = names
                        else:
                            names = self.env['ir.sequence'].next_by_code('branch.jakarta.virtus.wb.do')
                            this.name = names
                    

           
        
        return res
    
