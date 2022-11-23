
from odoo.exceptions import UserError
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime,timedelta

class ResPartner(models.Model):
    _inherit = 'stock.picking'
    
    invoice_id = fields.Many2one('account.move','No. Invoice')
    invoice_line_id = fields.Many2one('account.move.line')
    po_customer = fields.Char(String='Po Customer',related='sale_id.po_customer')
    temp_picking = fields.Char(string="picking ID",store=True)
    tanggal_diterima = fields.Date(string='Tanggal Diterima')
    address_del = fields.Char(Sting="Delivery Detail",related="partner_id.street")
    tanggal_so = fields.Datetime(string="tanggal SO",related="sale_id.date_order")
    total_cbm = fields.Float(string="total cbm",compute="get_total_cbm")


    states_tanggal = fields.Selection([
        ('done', 'Ready'),
        ('notready', 'Not Ready'),
    ], string='Status',
        copy=False, index=True, readonly=True, store=True, tracking=True,compute='tanggal_terima')
    states_picking = fields.Selection([
        ('incoming', 'Incoming'),
        ('outgoing', 'Outgoing'),
    ], string='Status',
        copy=False, index=True, readonly=True, store=True, tracking=True,compute='state_picking')
    states = fields.Selection([
        ('ready', 'Ready'),
        ('invoiced', 'Invoiced'),
    ], string='Status',
        copy=False, index=True, readonly=True, store=True, tracking=True,default='ready')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting'),
        ('assigned', 'Ready'),
        ('delivery', 'Delivery'),
        ('delivery_part', 'Delivery Partial'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', compute='_compute_state',
        copy=False, index=True, readonly=True, store=True, tracking=True,
        help=" * Draft: The transfer is not confirmed yet. Reservation doesn't apply.\n"
             " * Waiting another operation: This transfer is waiting for another operation before being ready.\n"
             " * Waiting: The transfer is waiting for the availability of some products.\n(a) The shipping policy is \"As soon as possible\": no product could be reserved.\n(b) The shipping policy is \"When all products are ready\": not all the products could be reserved.\n"
             " * Ready: The transfer is ready to be processed.\n(a) The shipping policy is \"As soon as possible\": at least one product has been reserved.\n(b) The shipping policy is \"When all products are ready\": all product have been reserved.\n"
             " * Done: The transfer has been processed.\n"
             " * Cancelled: The transfer has been cancelled.")

    def get_total_cbm(self):
        temp = 0
        total = 0
        self.total_cbm=0
        for this in self:
                for line in this.move_line_ids_without_package:
                    temp = line.qty_done * line.product_id.volume
                    total = temp + total
                    self.total_cbm = total
    
   
    @api.depends('tanggal_diterima')
    def tanggal_terima(self):
        for this in self:
            if this.tanggal_diterima != False:
                self.write({'states_tanggal': "done"})
            else:
                self.write({'states_tanggal': "notready"})
    @api.depends('picking_type_id')
    def state_picking(self):
        for this in self:
            if this.picking_type_id.code != 'outgoing':
                self.write({'states_picking': "incoming"})
            else:
                self.write({'states_picking': "outgoing"})
    
    def delivery_cancel(self):
        for i in self:
            i.write({'state': 'assigned'})

    def reset_to_ready(self):
        for i in self:
            i.write({'states': 'ready'})


    def delivery(self):
        today = datetime.today()
        for i in self:
            i.write({'state': 'delivery'})
            

    def delivery_part(self):
        today = datetime.today()
        for i in self:
            i.write({'state': 'delivery_part'})



    @api.onchange('create_invoices')
    def create_invoices(self):
        picking_id = self
        sale_orders = picking_id.sale_id
        sale_picking = sale_orders.picking_ids.filtered(lambda x: x.id == self.id)
        # print(sale_trying,"picking_test_get")
        if sale_picking:
            if self.state == 'done' :
                if self.picking_type_id.code == 'outgoing':
                    sale_orders._create_invoices_delivery_order(move_ids=sale_picking.move_ids_without_package,picking=sale_picking.name,picking_date=sale_picking.scheduled_date,terima=sale_picking.tanggal_diterima)
                self.write({'states': "invoiced"})
            if self._context.get('open_invoices', False):
                return sale_orders.action_view_invoice()
        

        return {'type': 'ir.actions.act_window_close'}


    def button_validate(self):
        res = super(ResPartner, self).button_validate()
        for this in self:
            if self.tanggal_diterima:
                for line in this.move_lines:
                    if line.date:
                        line.date= this.tanggal_diterima
                        for valuation in line.stock_valuation_layer_ids:
                            if valuation.product_id:
                                parameters= []
                                parameters.append(self.tanggal_diterima) # date to data
                                parameters.append(valuation.id) # object id

                                self.env.cr.execute("UPDATE public.stock_valuation_layer SET create_date=%s WHERE id=%s ",(parameters))

                for lines in this.move_line_ids:
                    if lines.date:
                        lines.write({'date': this.tanggal_diterima})
            
        return res
    