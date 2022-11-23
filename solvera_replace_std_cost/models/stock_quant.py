# -*- coding: utf-8 -*-
from collections import defaultdict
from itertools import product
from re import S
from string import digits
from unicodedata import digit

from odoo import api, models,fields,_
from odoo.exceptions import UserError
from odoo.tools import float_is_zero,float_round,float_compare


class StockMove(models.Model):
    _inherit = "stock.move"

    # valuation= fields.Monetary(string='Value')

    # def compute_valuation(self):
    #     for i in self:
    #         for this in i.move_line_ids:
    #             get_value = this.product_uom_qty*this.product_id

    def _get_price_unit(self):
        """ Returns the unit price for the move"""
        self.ensure_one()
        if self.purchase_line_id and self.product_id.id == self.purchase_line_id.product_id.id:
            price_unit_prec = self.env['decimal.precision'].precision_get('Product Price')
            line = self.purchase_line_id
            order = line.order_id
            price_unit = line.price_unit
            if line.taxes_id:
                qty = line.product_qty or 1
                price_unit = line.taxes_id.with_context(round=False).compute_all(price_unit, currency=line.order_id.currency_id, quantity=qty)['total_void']
                price_unit = float_round(price_unit / qty, precision_digits=price_unit_prec)
            if line.product_uom.id != line.product_id.uom_id.id:
                price_unit *= line.product_uom.factor / line.product_id.uom_id.factor
            if order.currency_id != order.company_id.currency_id:
                # The date must be today, and not the date of the move since the move move is still
                # in assigned state. However, the move date is the scheduled date until move is
                # done, then date of actual move processing. See:
                # https://github.com/odoo/odoo/blob/2f789b6863407e63f90b3a2d4cc3be09815f7002/addons/stock/models/stock_move.py#L36
                price_unit = order.currency_id._convert(
                    price_unit, order.company_id.currency_id, order.company_id, fields.Date.context_today(self), round=False)
            print(fields.Date.context_today,'cekprint_stock')
            return price_unit
        return super(StockMove, self)._get_price_unit()


    def product_price_update_before_done(self, forced_qty=None):
        tmpl_dict = defaultdict(lambda: 0.0)
        # adapt standard price on incomming moves if the product cost_method is 'average'
        std_price_update = {}
        quant_obj = self.env['stock.location'].search([('branch_id','=',self.branch_id.id)])
        product_tot_qty_available_branch = 0
        rate=self.env['res.currency.rate'].search([('currency_id','=',self.picking_id.purchase_id.currency_id.id),('name','<=',self.picking_id.purchase_id.date_order)], limit=1, order='create_date desc')
        currency_rate = int(rate.rate)
        for move in self.filtered(lambda move: move.location_id.usage in ('supplier', 'production') and move.product_id.cost_method in ('average', 'last','branch')):
            if move.picking_code == 'incoming':
                print('problem')   
                product_tot_qty_available = move.product_id.qty_available + tmpl_dict[move.product_id.id]
                rounding = move.product_id.uom_id.rounding
                for this in quant_obj:
                    for line in this.quant_ids:
                        if move.product_id.id == line.product_id.id:
                            product_tot_qty_available_branch = line.quantity

                qty_done = 0.0
                if float_is_zero(product_tot_qty_available, precision_rounding=rounding):
                    new_std_price = move._get_price_unit()
                elif float_is_zero(product_tot_qty_available + move.product_qty, precision_rounding=rounding) or \
                        float_is_zero(product_tot_qty_available + qty_done, precision_rounding=rounding):
                    new_std_price = move._get_price_unit()
                else:
                    # Get the standard price
                    if move.product_id.cost_method == 'average':
                        amount_unit = std_price_update.get(
                            (move.company_id.id, move.product_id.id)) or move.product_id.standard_price
                        qty_done = move.product_uom._compute_quantity(move.quantity_done, move.product_id.uom_id)
                        qty = forced_qty or qty_done
                    if move.product_id.cost_method == 'branch':
                        if self.branch_id.id == 1 :
                            if float_is_zero(product_tot_qty_available_branch, precision_rounding=rounding):
                                new_std_price = move._get_price_unit()

                            else:
                                amount_unit = std_price_update.get(
                                    (move.company_id.id, move.product_id.id)) or move.product_id.standard_price_jakarta
                                qty_done = move.product_uom._compute_quantity(move.quantity_done, move.product_id.uom_id)
                                qty = forced_qty or qty_done
                                new_std_price = ((amount_unit * product_tot_qty_available_branch) + (move._get_price_unit() * qty)) / (product_tot_qty_available_branch + qty_done)
                        elif self.branch_id.id == 2 :
                            if float_is_zero(product_tot_qty_available_branch, precision_rounding=rounding):
                                new_std_price = move._get_price_unit()
                            else:
                                amount_unit = std_price_update.get(
                                    (move.company_id.id, move.product_id.id)) or move.product_id.standard_price_surabaya
                                qty_done = move.product_uom._compute_quantity(move.quantity_done, move.product_id.uom_id)
                                qty = forced_qty or qty_done
                                new_std_price = ((amount_unit * product_tot_qty_available_branch) + (move._get_price_unit() * qty)) / (product_tot_qty_available_branch + qty_done)
                        elif self.branch_id.id == 3 :
                            if float_is_zero(product_tot_qty_available_branch, precision_rounding=rounding):
                                new_std_price = move._get_price_unit()

                            else:
                                amount_unit = std_price_update.get(
                                    (move.company_id.id, move.product_id.id)) or move.product_id.standard_price_bali
                                qty_done = move.product_uom._compute_quantity(move.quantity_done, move.product_id.uom_id)
                                qty = forced_qty or qty_done
                                new_std_price = ((amount_unit * product_tot_qty_available_branch) + (move._get_price_unit() * qty)) / (product_tot_qty_available_branch + qty_done)
                        else:
                            amount_unit = (std_price_update.get(
                                (move.company_id.id, move.product_id.id)) or move.product_id.standard_price)
                            qty_done = move.product_uom._compute_quantity(move.quantity_done, move.product_id.uom_id)
                            qty = forced_qty or qty_done
                            new_std_price = ((amount_unit * product_tot_qty_available) + (move._get_price_unit() * qty)) / (product_tot_qty_available + qty_done)

                if move.product_id.cost_method == 'last' and move.product_id.valuation == 'real_time':
                    new_std_price = move._get_price_unit()
                    products = self.env['product.product'].browse(move.product_id.id)
                    account_id = products.property_account_creditor_price_difference.id or products.categ_id.property_account_creditor_price_difference_categ.id
                    if not account_id:
                        raise UserError(_('Configuration error. Please configure the price difference account on the product or its category to process this operation.'))
                    products.create_price_change_account_move(new_std_price, account_id, move.company_id.id, move.origin)
                tmpl_dict[move.product_id.id] += qty_done
                # Write the standard price, as SUPERUSER_ID because a warehouse manager may not have the right to write on products
                if move.product_id.cost_method == 'branch':
                    if self.branch_id.id == 1:
                        move.product_id.with_context(with_company=move.company_id.id).sudo().write({'standard_price_jakarta': new_std_price})
                    elif self.branch_id.id == 2:
                        move.product_id.with_context(with_company=move.company_id.id).sudo().write({'standard_price_surabaya': new_std_price})
                    elif self.branch_id.id == 3:
                        move.product_id.with_context(with_company=move.company_id.id).sudo().write({'standard_price_bali': new_std_price})
                    else:
                        move.product_id.with_context(with_company=move.company_id.id).sudo().write({'standard_price': new_std_price})
                else:
                    move.product_id.with_context(with_company=move.company_id.id).sudo().write({'standard_price': new_std_price/currency_rate})
                std_price_update[move.company_id.id, move.product_id.id] = new_std_price


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'


    def write(self, vals):
        """ When editing a done stock.move.line, we impact the valuation. Users may increase or
        decrease the `qty_done` field. There are three cost method available: standard, average
        and fifo. We implement the logic in a similar way for standard and average: increase
        or decrease the original value with the standard or average price of today. In fifo, we
        have a different logic wheter the move is incoming or outgoing. If the move is incoming, we
        update the value and remaining_value/qty with the unit price of the move. If the move is
        outgoing and the user increases qty_done, we call _run_fifo and it'll consume layer(s) in
        the stack the same way a new outgoing move would have done. If the move is outoing and the
        user decreases qty_done, we either increase the last receipt candidate if one is found or
        we decrease the value with the last fifo price.
        """
        if 'qty_done' in vals:
            moves_to_update = {}
            for move_line in self.filtered(
                    lambda ml: ml.state == 'done' and (ml.move_id._is_in() or ml.move_id._is_out())):
                moves_to_update[move_line.move_id] = vals['qty_done'] - move_line.qty_done

            for move_id, qty_difference in moves_to_update.items():
                move_vals = {}
                if move_id.product_id.cost_method in ['standard', 'average', 'last']:
                    correction_value = qty_difference * move_id.product_id.standard_price
                    if move_id._is_in():
                        move_vals['value'] = move_id.value + correction_value
                    elif move_id._is_out():
                        move_vals['value'] = move_id.value - correction_value
                elif move_id.product_id.cost_method == 'branch':
                    if self.branch_id.id == 1:
                        correction_value = qty_difference * move_id.product_id.standard_price_jakarta
                        if move_id._is_in():
                            move_vals['value'] = move_id.value + correction_value
                        elif move_id._is_out():
                            move_vals['value'] = move_id.value - correction_value
                    elif self.branch_id.id == 2:
                        correction_value = qty_difference * move_id.product_id.standard_price_surabaya
                        if move_id._is_in():
                            move_vals['value'] = move_id.value + correction_value
                        elif move_id._is_out():
                            move_vals['value'] = move_id.value - correction_value
                    elif self.branch_id.id == 3:
                        correction_value = qty_difference * move_id.product_id.standard_price_bali
                        if move_id._is_in():
                            move_vals['value'] = move_id.value + correction_value
                        elif move_id._is_out():
                            move_vals['value'] = move_id.value - correction_value
                    else:
                        correction_value = qty_difference * move_id.product_id.standard_price
                        if move_id._is_in():
                            move_vals['value'] = move_id.value + correction_value
                        elif move_id._is_out():
                            move_vals['value'] = move_id.value - correction_value
                else:
                    if move_id._is_in():
                        correction_value = qty_difference * move_id.price_unit
                        new_remaining_value = move_id.remaining_value + correction_value
                        move_vals['value'] = move_id.value + correction_value
                        move_vals['remaining_qty'] = move_id.remaining_qty + qty_difference
                        move_vals['remaining_value'] = move_id.remaining_value + correction_value
                    elif move_id._is_out() and qty_difference > 0:
                        correction_value = self.env['stock.move']._run_fifo(move_id, quantity=qty_difference)
                        # no need to adapt `remaining_qty` and `remaining_value` as `_run_fifo` took care of it
                        move_vals['value'] = move_id.value - correction_value
                    elif move_id._is_out() and qty_difference < 0:
                        candidates_receipt = self.env['stock.move'].search(move_id._get_in_domain(), order='date, id desc', limit=1)
                        if candidates_receipt:
                            candidates_receipt.write({
                                'remaining_qty': candidates_receipt.remaining_qty + -qty_difference,
                                'remaining_value': candidates_receipt.remaining_value + (
                                -qty_difference * candidates_receipt.price_unit),
                            })
                            correction_value = qty_difference * candidates_receipt.price_unit
                        else:
                            correction_value = qty_difference * move_id.product_id.standard_price
                        move_vals['value'] = move_id.value - correction_value
                move_id.write(move_vals)

                if move_id.product_id.valuation == 'real_time':
                    move_id.with_context(force_valuation_amount=correction_value, forced_quantity=qty_difference)._account_entry_move()
                if qty_difference > 0:
                    move_id.product_price_update_before_done(forced_qty=qty_difference)
        return super(StockMoveLine, self).write(vals)

class StockLocation(models.Model):
    _inherit = 'stock.location'
   
    @api.model
    def _get_default_branch(self):
        """methode to get default branch"""
        branch_id = self.env.user.branch_id
        return branch_id

    def _get_branch_domain(self):
        """methode to get branch domain"""
        company = self.env.company
        branch_ids = self.env.user.branch_ids
        branch = branch_ids.filtered(
            lambda branch: branch.company_id == company)
        return [('id', 'in', branch.ids)]

    branch_id = fields.Many2one('res.branch', string='Branch', store=True,
                                default=_get_default_branch,
                                domain=_get_branch_domain,
                                help='Leave this field empty if this warehouse '
                                     ' is shared between all branches')



class StockQuant(models.Model):
    _inherit = 'stock.quant'

    def _set_inventory_quantity(self):
        """ Inverse method to create stock move when `inventory_quantity` is set
        (`inventory_quantity` is only accessible in inventory mode).
        """
        if not self._is_inventory_mode():
            return
        for quant in self:
            # Get the quantity to create a move for.
            rounding = quant.product_id.uom_id.rounding
            diff = float_round(quant.inventory_quantity - quant.quantity, precision_rounding=rounding)
            diff_float_compared = float_compare(diff, 0, precision_rounding=rounding)
            # Create and vaidate a move so that the quant matches its `inventory_quantity`.
            if diff_float_compared == 0:
                continue
            elif diff_float_compared > 0:
                move_vals = quant._get_inventory_move_values(diff, quant.product_id.with_company(quant.company_id).property_stock_inventory, quant.location_id)
            else:
                move_vals = quant._get_inventory_move_values(-diff, quant.location_id, quant.product_id.with_company(quant.company_id).property_stock_inventory, out=True)
            move = quant.env['stock.move'].with_context(inventory_mode=False).create(move_vals)
            move._action_done()
            if quant.product_id.cost_method =='branch':
                svl_obj =self.env['stock.valuation.layer'].sudo().search([('stock_move_id','=',move.id)])
                if quant.location_id.branch_id.id == 1:
                    price = quant.product_id.standard_price_jakarta *svl_obj.quantity
                    svl_obj.sudo().write({
                                    'unit_cost': quant.product_id.standard_price_jakarta,
                                    'value': price,
                                    'branch_id':quant.location_id.branch_id.id
                                
                                })
                if quant.location_id.branch_id.id == 2:
                    price = quant.product_id.standard_price_surabaya *svl_obj.quantity
                    svl_obj.sudo().write({
                                    'unit_cost': quant.product_id.standard_price_surabaya,
                                    'value': price,
                                    'branch_id':quant.location_id.branch_id.id
                                
                                })
                if quant.location_id.branch_id.id == 3:
                    price = quant.product_id.standard_price_bali *svl_obj.quantity
                    svl_obj.sudo().write({
                                    'unit_cost': quant.product_id.standard_price_bali,
                                    'value': price,
                                    'branch_id':quant.location_id.branch_id.id
                                
                                })
            else:
                continue

    @api.depends('company_id', 'location_id', 'owner_id', 'product_id', 'quantity')
    def _compute_value(self):
        """ For standard and AVCO valuation, compute the current accounting
        valuation 78,78,of the quants by multiplying the quantity by
        the standard price. Instead for FIFO, use the quantity times the
        average cost (valuation layers are not manage by location so the
        average cost is the same for all location and the valuation field is
        a estimation more than a real value).
        """
        self.currency_id = self.env.company.currency_id
        print('cek_problem_price2')
        for quant in self:
            # If the user didn't enter a location yet while enconding a quant.
            if not quant.location_id:
                quant.value = 0
                return

            if not quant.location_id._should_be_valued() or\
                    (quant.owner_id and quant.owner_id != quant.company_id.partner_id):
                quant.value = 0
                continue
            if quant.product_id.cost_method == 'fifo':
                quantity = quant.product_id.quantity_svl
                if float_is_zero(quantity, precision_rounding=quant.product_id.uom_id.rounding):
                    quant.value = 0.0
                    continue
                average_cost = quant.product_id.value_svl / quantity
                quant.value = quant.quantity * average_cost
            elif quant.product_id.cost_method == 'branch':
                quantity = quant.product_id.quantity_svl
                if float_is_zero(quantity, precision_rounding=quant.product_id.uom_id.rounding):
                    quant.value = 0.0
                    continue
                elif quant.location_id.branch_id.id == 1:
                    average_cost = quant.product_id.standard_price_jakarta 
                    quant.value = quant.quantity * average_cost
                elif quant.location_id.branch_id.id == 2:
                    average_cost = quant.product_id.standard_price_surabaya 
                    quant.value = quant.quantity * average_cost
                elif quant.location_id.branch_id.id == 3:
                    average_cost = quant.product_id.standard_price_bali 
                    quant.value = quant.quantity * average_cost
                else:
                    average_cost = quant.product_id.value_svl / quantity
            else:
                quant.value = quant.quantity * quant.product_id.standard_price


class StockQuant(models.Model):
    _inherit = 'stock.inventory'


    def action_validate(self):
        if not self.exists():
            return
        self.ensure_one()
        if not self.user_has_groups('stock.group_stock_manager'):
            raise UserError(_("Only a stock manager can validate an inventory adjustment."))
        if self.state != 'confirm':
            raise UserError(_(
                "You can't validate the inventory '%s', maybe this inventory "
                "has been already validated or isn't ready.", self.name))
        inventory_lines = self.line_ids.filtered(lambda l: l.product_id.tracking in ['lot', 'serial'] and not l.prod_lot_id and l.theoretical_qty != l.product_qty)
        lines = self.line_ids.filtered(lambda l: float_compare(l.product_qty, 1, precision_rounding=l.product_uom_id.rounding) > 0 and l.product_id.tracking == 'serial' and l.prod_lot_id)
        if inventory_lines and not lines:
            wiz_lines = [(0, 0, {'product_id': product.id, 'tracking': product.tracking}) for product in inventory_lines.mapped('product_id')]
            wiz = self.env['stock.track.confirmation'].create({'inventory_id': self.id, 'tracking_line_ids': wiz_lines})
            return {
                'name': _('Tracked Products in Inventory Adjustment'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'views': [(False, 'form')],
                'res_model': 'stock.track.confirmation',
                'target': 'new',
                'res_id': wiz.id,
            }
        self._action_done()
        self.line_ids._check_company()
        self._check_company()
        self.valuation_branch()
        return True

    def valuation_branch(self):
        print('test_print_val_0')
        for this in self:
            account_move = self.env['account.move']
            for line in this.move_ids:
                svl_obj = self.env['stock.valuation.layer'].sudo().search([('stock_move_id','=',line.id)])
                if line.product_id.cost_method == 'branch':
                    if line.location_id.branch_id.id==1:
                        price = line.product_id.standard_price_jakarta *svl_obj.quantity
                        
                        move_lines = [
                        (0, 0, {
                            'account_id':line.product_id.categ_id.property_stock_valuation_account_id.id,
                            'name': str(self.name)+' - '+line.product_id.name,
                            'credit':price*-1,
                            'currency_id':self.company_id.currency_id.id,
                        }),
                        (0, 0, {
                            'account_id':line.product_id.categ_id.property_stock_account_output_categ_id.id,
                            'name': str(self.name)+' - '+line.product_id.name,
                            'debit':price*-1,
                            'currency_id':self.company_id.currency_id.id,
                        }),
                        ]
                        move_id = account_move.create({
                            'ref':str(self.name)+' - '+line.product_id.name,
                            'date':line.create_date,
                            'journal_id':6,
                            'line_ids': move_lines,
                            'branch_id':line.location_id.branch_id,
                            'stock_move_id':line._origin.id
                        })
                        move_id.post()
                        svl_obj.sudo().write({
                                    'unit_cost': line.product_id.standard_price_jakarta,
                                    'value': price*-1,
                                    'branch_id':line.location_id.branch_id.id,
                                    'stock_move_id':line._origin.id,
                                    'account_move_id':move_id.id,
                                
                                })

                    elif line.location_id.branch_id.id==2:
                        price = line.product_id.standard_price_surabaya *svl_obj.quantity
                        

                        move_lines = [
                        (0, 0, {
                            'account_id':line.product_id.categ_id.property_stock_valuation_account_id.id,
                            'name': str(self.name)+' - '+line.product_id.name,
                            'credit':price*-1,
                            'currency_id':self.company_id.currency_id.id,
                        }),
                        (0, 0, {
                            'account_id':line.product_id.categ_id.property_stock_account_output_categ_id.id,
                            'name': str(self.name)+' - '+line.product_id.name,
                            'debit':price*-1,
                            'currency_id':self.company_id.currency_id.id,
                        }),
                        ]
                        move_id = account_move.create({
                            'ref':str(self.name)+' - '+line.product_id.name,
                            'date':line.create_date,
                            'journal_id':6,
                            'line_ids': move_lines,
                            'branch_id':line.location_id.branch_id,
                            'stock_move_id':line._origin.id
                        })
                        move_id.post()
                        svl_obj.sudo().write({
                                    'unit_cost': line.product_id.standard_price_surabaya,
                                    'value': price*-1,
                                    'branch_id':line.location_id.branch_id.id,
                                    'stock_move_id':line._origin.id,
                                    'account_move_id':move_id.id,
                                
                                })

                    elif line.location_id.branch_id.id==3:
                        price = line.product_id.standard_price_bali *svl_obj.quantity
                        
                        move_lines = [
                        (0, 0, {
                            'account_id':line.product_id.categ_id.property_stock_valuation_account_id.id,
                            'name': str(self.name)+' - '+line.product_id.name,
                            'credit':price*-1,
                            'currency_id':self.company_id.currency_id.id,
                        }),
                        (0, 0, {
                            'account_id':line.product_id.categ_id.property_stock_account_output_categ_id.id,
                            'name': str(self.name)+' - '+line.product_id.name,
                            'debit':price*-1,
                            'currency_id':self.company_id.currency_id.id,
                        }),
                        ]
                        move_id = account_move.create({
                            'ref':str(self.name)+' - '+line.product_id.name,
                            'date':line.create_date,
                            'journal_id':6,
                            'line_ids': move_lines,
                            'branch_id':line.location_id.branch_id,
                            'stock_move_id':line._origin.id
                        })
                        move_id.post()
                        svl_obj.sudo().write({
                                    'unit_cost': line.product_id.standard_price_bali,
                                    'value': price*-1,
                                    'branch_id':line.location_id.branch_id.id,
                                    'stock_move_id':line._origin.id,
                                    'account_move_id':move_id.id,
                                
                                })
                    elif line.location_dest_id.branch_id.id==1:
                        price = line.product_id.standard_price_jakarta *svl_obj.quantity
                       
                        move_lines = [
                        (0, 0, {
                            'account_id':line.product_id.categ_id.property_stock_valuation_account_id.id,
                            'name': str(self.name)+' - '+line.product_id.name,
                            'credit':price,
                            'currency_id':self.company_id.currency_id.id,
                        }),
                        (0, 0, {
                            'account_id':line.product_id.categ_id.property_stock_account_output_categ_id.id,
                            'name': str(self.name)+' - '+line.product_id.name,
                            'debit':price,
                            'currency_id':self.company_id.currency_id.id,
                        }),
                        ]
                        move_id = account_move.create({
                            'ref':str(self.name)+' - '+line.product_id.name,
                            'date':line.create_date,
                            'journal_id':6,
                            'line_ids': move_lines,
                            'branch_id':line.location_id.branch_id,
                            'stock_move_id':line._origin.id
                        })
                        move_id.post()
                        svl_obj.sudo().write({
                                    'unit_cost': line.product_id.standard_price_jakarta,
                                    'value': price,
                                    'branch_id':line.location_id.branch_id.id,
                                    'stock_move_id':line._origin.id,
                                    'account_move_id':move_id.id,
                                
                                })
                    elif line.location_dest_id.branch_id.id==2:
                        price = line.product_id.standard_price_surabaya *svl_obj.quantity
                       
                        move_lines = [
                        (0, 0, {
                            'account_id':line.product_id.categ_id.property_stock_valuation_account_id.id,
                            'name': str(self.name)+' - '+line.product_id.name,
                            'credit':price,
                            'currency_id':self.company_id.currency_id.id,
                        }),
                        (0, 0, {
                            'account_id':line.product_id.categ_id.property_stock_account_output_categ_id.id,
                            'name': str(self.name)+' - '+line.product_id.name,
                            'debit':price,
                            'currency_id':self.company_id.currency_id.id,
                        }),
                        ]
                        move_id = account_move.create({
                            'ref':str(self.name)+' - '+line.product_id.name,
                            'date':line.create_date,
                            'journal_id':6,
                            'line_ids': move_lines,
                            'branch_id':line.location_id.branch_id,
                            'stock_move_id':line._origin.id
                        })
                        move_id.post()
                        svl_obj.sudo().write({
                                    'unit_cost': line.product_id.standard_price_surabaya,
                                    'value': price,
                                    'branch_id':line.location_id.branch_id.id,
                                    'stock_move_id':line._origin.id,
                                    'account_move_id':move_id.id,
                                })
                    elif line.location_dest_id.branch_id.id==3:
                        price = line.product_id.standard_price_bali *svl_obj.quantity

                        move_lines = [
                        (0, 0, {
                            'account_id':line.product_id.categ_id.property_stock_valuation_account_id.id,
                            'name': str(self.name)+' - '+line.product_id.name,
                            'credit':price,
                            'currency_id':self.company_id.currency_id.id,
                        }),
                        (0, 0, {
                            'account_id':line.product_id.categ_id.property_stock_account_output_categ_id.id,
                            'name': str(self.name)+' - '+line.product_id.name,
                            'debit':price,
                            'currency_id':self.company_id.currency_id.id,
                        }),
                        ]
                        move_id = account_move.create({
                            'ref':str(self.name)+' - '+line.product_id.name,
                            'date':line.create_date,
                            'journal_id':6,
                            'line_ids': move_lines,
                            'branch_id':line.location_id.branch_id,
                            'stock_move_id':line._origin.id
                        })
                        move_id.post()
                        svl_obj.sudo().write({
                                    'unit_cost': line.product_id.standard_price_bali,
                                    'value': price,
                                    'branch_id':line.location_id.branch_id.id,
                                    'stock_move_id':line._origin.id,
                                    'account_move_id':move_id.id,
                                
                                })
                    else:
                        continue
# class SVL(models.Model):
#     _inherit = 'stock.valuation.layer'                 

#     unit_cost = fields.Monetary('Unit Value',readonly=False,digits="idr")
            
