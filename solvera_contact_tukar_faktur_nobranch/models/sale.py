

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime,timedelta
from odoo.exceptions import UserError

class ResPartner(models.Model):
    _inherit = 'sale.order'
    
    tukar_faktur_allowed = fields.Boolean(string='Customer tukar faktur', related="partner_id.tukar_faktur_allow")
    get_do=fields.Char()
    date_dev = fields.Datetime()
    terima = fields.Date()
    po_customer = fields.Char(string='Po Customer')
    address_inv = fields.Char(string="Invoice Detail",related="partner_invoice_id.street")
    address_del = fields.Char(sting="Delivery Detail",related="partner_shipping_id.street")
    state_sale = fields.Selection([
    ('0', 'Offline'),
    ('1', 'Tokopedia'),
    ('2', 'Shopee'),
    ('3', 'Lazada'),
    ('4', 'Web'),
    ], string='Sumber Penjualan', readonly=False, copy=False, related="partner_id.state_sale")

    def _create_invoices_delivery_order(self,picking,terima,picking_date, grouped=False, final=False,move_ids=False):
        """
        Create the invoice associated to the SO.
        :param grouped: if True, invoices are grouped by SO id. If False, invoices are grouped by
                        (partner_invoice_id, currency)
        :param final: if True, refunds will be generated if necessary
        :returns: list of created invoices
        """
        for each in self:
            if not self.env['account.move'].check_access_rights('create', False):
                try:
                    self.check_access_rights('write')
                    self.check_access_rule('write')
                except AccessError:

                    return self.env['account.move']

            precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')

            # 1) Create invoices.
            invoice_vals_list = []
            for order in self:
                self.get_do = picking
                self.date_dev = picking_date
                self.terima = terima
                pending_section = None
                
                invoice_vals = order._prepare_invoice()

                # Invoice line values (keep only necessary sections).
                for line in order.order_line:
                    if line.display_type == 'line_section':
                        pending_section = line
                        continue
                    # move_ids = self.env['stock.picking']
                    moves = move_ids.filtered(lambda x: x.product_id.id == line.product_id.id and x.sale_line_id.id == line.id and x.quantity_done > 0)
                    for move in moves:
                        if line.qty_to_invoice > 0 or (line.qty_to_invoice < 0 and final):
                            if pending_section:
                                invoice_vals['invoice_line_ids'].append((0, 0, pending_section._prepare_invoice_lines()))
                                pending_section = None           
                            invoice_vals['invoice_line_ids'].append((0, 0, line._prepare_invoice_lines(move)))

                if not invoice_vals['invoice_line_ids']:
                    raise UserError(('There is no invoiceable line. If a product has a Delivered quantities invoicing policy, please make sure that a quantity has been delivered.'))

                invoice_vals_list.append(invoice_vals)

            if not invoice_vals_list:
                raise UserError((
                    'There is no invoiceable line. If a product has a Delivered quantities invoicing policy, please make sure that a quantity has been delivered.'))

            # 3) Create invoices.
            # Manage the creation of invoices in sudo because a salesperson must be able to generate an invoice from a
            # sale order without "billing" access rights. However, he should not be able to create an invoice from scratch.
            moves = self.env['account.move'].sudo().with_context(default_type='out_invoice').create(invoice_vals_list)
            
            # for invoice in moves:
            #     invoice._onchange_partner_id()
            # moves._onchange_partner_id()
            # Some moves might actually be refunds: convert them if the total amount is negative
            # We do this after the moves have been created since we need taxes, etc. to know if the total
            # is actually negative or not
            if final:
                moves.sudo().filtered(lambda m: m.amount_total < 0).action_switch_invoice_into_refund_credit_note()
            for move in moves:
                move.message_post_with_view('mail.message_origin_link',
                    values={'self': move, 'origin': move.line_ids.mapped('sale_line_ids.order_id')},
                    subtype_id=self.env.ref('mail.mt_note').id
                )
            # Update Stock move with no Invoice supaya tidak ditarik lagi
            
 
        
            moves.invoice_line_ids.picking_ids.invoice_id = moves.id
            # stock_move_ids.invoice_id = moves.id
            ##replace journal untuk sumber pembelian
            for i in self:
                if i.state_sale == '1':
                    for line in i.order_line:
                        for lines in i.invoice_ids:
                            for inv in lines.line_ids:
                                if line.product_id.categ_id.property_account_income_categ_id == inv.account_id:
                                    inv.update({
                                            'account_id': line.product_id.categ_id.property_account_income_toped_categ_id,
                                        })
                if i.state_sale == '2':
                    for line in i.order_line:
                        for lines in i.invoice_ids:
                            for inv in lines.line_ids:
                                if line.product_id.categ_id.property_account_income_categ_id == inv.account_id:
                                    inv.update({
                                            'account_id': line.product_id.categ_id.property_account_income_shoppe_categ_id,
                                        })
                if i.state_sale == '3':
                    for line in i.order_line:
                        for lines in i.invoice_ids:
                            for inv in lines.line_ids:
                                if line.product_id.categ_id.property_account_income_categ_id == inv.account_id:
                                    inv.update({
                                            'account_id': line.product_id.categ_id.property_account_income_lazada_categ_id,
                                        })

                if i.state_sale == '4':
                    for line in i.order_line:
                        for lines in i.invoice_ids:
                            for inv in lines.line_ids:
                                if line.product_id.categ_id.property_account_income_categ_id == inv.account_id:
                                    inv.update({
                                            'account_id': line.product_id.categ_id.property_account_income_web_categ_id,
                                        })

            return moves



class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    po_customer = fields.Char(String='Po Customer',related='order_id.po_customer')
    fix_discount= fields.Float('Fix Discount')
    is_fix_discount=fields.Boolean('Fix Discount')
    state_sale = fields.Selection([
    ('0', 'Offline'),
    ('1', 'Tokopedia'),
    ('2', 'Shopee'),
    ('3', 'Lazada'),
    ('4', 'Web'),
    ], string='Sumber Penjualan', readonly=False, copy=False, related="order_id.state_sale")
    def _prepare_invoice_lines(self,move=None):
        """
        Prepare the dict of values to create the new invoice line for a sales order line.

        :param qty: float quantity to invoice
        """
        self.ensure_one()
        stock_move_obj = self.env['stock.move']
        picking_ids = self.order_id.picking_ids.filtered(lambda pick: pick.state=="done")
        move_ids = stock_move_obj.search([('picking_id','in',picking_ids.ids if picking_ids else []), ('invoice_id','=', False)])
        moves = move_ids.filtered(lambda x: x.product_id.id == self.product_id.id)
        picking_id = moves.mapped('picking_id').ids if moves else False
        picking_line_id = moves.mapped('id') if moves else False
        
        qty = move.quantity_done if move else self.qty_to_invoice
        res = {
            'display_type': self.display_type,
            'sequence': self.sequence,
            'state_sale':self.state_sale,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom.id,
            'quantity': qty,
            'discount': self.discount,
            'price_unit': self.price_unit,
            'discount_fixed': self.discount_fixed,
            'picking': self.order_id.get_do,
            'date_validate': self.order_id.terima,
            'po_customer': self.po_customer,
            'is_fix_discount':self.is_fix_discount,
            'fix_discount':self.fix_discount,
            'picking_date': self.order_id.date_dev,
            'tax_ids': [(6, 0, self.tax_id.ids)],
            'sale_line_ids': [(4, self.id)],
            'picking_ids': [(6,0,picking_id)],
            'picking_line_ids': [(6,0,picking_line_id)]
        }
        if self.display_type:
            res['account_id'] = False
        return res
    