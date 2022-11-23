
import datetime
from itertools import product
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime,timedelta
from odoo.exceptions import UserError
from odoo.tools import float_is_zero,float_compare

class StockPicking(models.Model):
    _inherit = 'stock.picking'


    def update_stock(self):
        print('test_print_0')
        for i in self:
            for line in i.move_line_ids_without_package:
                not_product = line.location_dest_id.quant_ids.filtered(lambda x:x.product_id.id == line.product_id.id).sudo()
                if line.location_id.branch_id.id == 1:
                    if line.location_dest_id.branch_id.id == 2:
                        temp = 0
                        for lines in not_product:
                            get_quant = lines.quantity
                            jakarta_price = (line.qty_done*line.product_id.standard_price_jakarta)
                            val=(get_quant*self.product_id.standard_price_surabaya)
                            new_std_price_surabaya = (jakarta_price+val)/(line.qty_done+get_quant)
                            line.product_id.standard_price_surabaya = new_std_price_surabaya
                            temp = temp+1
                        if temp ==0:
                             line.product_id.standard_price_surabaya = line.product_id.standard_price_jakarta

                    if line.location_dest_id.branch_id.id == 3:
                        temp = 0
                        for lines in not_product:
                            get_quant = lines.quantity
                            jakarta_price = (line.qty_done*line.product_id.standard_price_jakarta)
                            val=(get_quant*self.product_id.standard_price_bali)
                            new_std_price_bali = (jakarta_price+val)/(line.qty_done+get_quant)
                            line.product_id.standard_price_bali = new_std_price_bali
                            temp = temp+1
                        if temp ==0:
                             line.product_id.standard_price_bali = line.product_id.standard_price_jakarta
                              
                ### From Surabaya
                elif line.location_id.branch_id.id == 2:
                    if line.location_dest_id.branch_id.id == 1:
                        temp = 0
                        for lines in not_product:
                            get_quant = lines.quantity
                            surabaya_price = (line.qty_done*line.product_id.standard_price_surabaya)
                            new_std_price_jakarta = (surabaya_price+lines.value)/(line.qty_done+get_quant)
                            line.product_id.standard_price_jakarta = new_std_price_jakarta
                            temp = temp+1
                        if temp ==0:
                            line.product_id.standard_price_jakarta = line.product_id.standard_price_surabaya
                                
                    if line.location_dest_id.branch_id.id == 3:
                        temp = 0
                        for lines in not_product:
                            get_quant = lines.quantity
                            surabaya_price = (line.qty_done*line.product_id.standard_price_surabaya)
                            new_std_price_bali = (surabaya_price+lines.value)/(line.qty_done+get_quant)
                            line.product_id.standard_price_bali = new_std_price_bali
                            temp = temp+1
                        if temp ==0:
                            line.product_id.standard_price_bali = line.product_id.standard_price_surabaya 
                
                ### From bali
                elif line.location_id.branch_id.id == 3:
                    if line.location_dest_id.branch_id.id == 1:
                        temp = 0
                        for lines in not_product:
                            get_quant = lines.quantity
                            bali_price = (line.qty_done*line.product_id.standard_price_bali)
                            new_std_price_jakarta = (bali_price+lines.value)/(line.qty_done+get_quant)
                            line.product_id.standard_price_jakarta = new_std_price_jakarta
                            temp = temp+1

                            if temp ==0:
                                line.product_id.standard_price_jakarta = line.product_id.standard_price_bali

                    if line.location_dest_id.branch_id.id == 2:
                        temp = 0
                        for lines in not_product:
                            get_quant = lines.quantity
                            bali_price = (line.qty_done*line.product_id.standard_price_bali)
                            new_std_price_surabaya = (bali_price+lines.value)/(line.qty_done+get_quant)
                            line.product_id.standard_price_surabaya = new_std_price_surabaya
                            temp = temp+1

                        if temp ==0:
                            line.product_id.standard_price_surabaya = line.product_id.standard_price_bali
                        

                else:
                    continue
                    


    def update_valuation(self):
        move_obj=self.env['account.move']
        print('test_print_1')
        for this in self:
            for line in this.move_lines:
                vl_object= self.env['stock.valuation.layer'].sudo().search([('stock_move_id','=',line._origin.id)])
                for lines in line.stock_valuation_layer_ids:
                    if this.branch_id.id == 1:
                        price = line.product_id.standard_price_jakarta *lines.quantity
                        if line.product_id == lines.product_id:
                            if vl_object.account_move_id:
                                vl_object.sudo().write({
                                    'unit_cost': line.product_id.standard_price_jakarta,
                                    'value': price
                                
                                })
                            else:
                                stock_move_obj = self.env['stock.move'].search([('id','=',line._origin.id)])
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
                                move_id = move_obj.sudo().create({
                                    'ref':str(self.name)+' - '+line.product_id.name,
                                    'date':lines.create_date,
                                    'journal_id':6,
                                    'line_ids': move_lines,
                                    'branch_id':self.branch_id.id,
                                    'stock_move_id':line._origin.id
                                })
                                vl_object.sudo().write({
                                    'unit_cost': line.product_id.standard_price_jakarta,
                                    'value': price,
                                    'account_move_id':move_id.id,
                                    'branch_id':line.branch_id
                                
                                })
                                move_id.sudo().post()
                               
                                

                    elif this.branch_id.id == 2:
                        price = line.product_id.standard_price_surabaya *lines.quantity
                        if line.product_id == lines.product_id:
                            if vl_object.account_move_id:
                                    vl_object.sudo().write({
                                        'unit_cost': line.product_id.standard_price_surabaya,
                                        'value': price
                                    
                                    })
                            else:
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
                                move_id = move_obj.sudo().create({
                                    'ref':str(self.name)+' - '+line.product_id.name,
                                    'date':lines.create_date,
                                    'journal_id':6,
                                    'line_ids': move_lines,
                                    'branch_id':self.branch_id.id,
                                    'stock_move_id':line._origin.id
                                })
                                vl_object.sudo().write({
                                    'unit_cost': line.product_id.standard_price_surabaya,
                                    'value': price,
                                    'account_move_id':move_id.id,
                                    'branch_id':line.branch_id
                                
                                })
                                move_id.sudo().post()
                                
                    elif this.branch_id.id == 3:
                        price = line.product_id.standard_price_bali *lines.quantity
                        if line.product_id == lines.product_id:
                            if vl_object.account_move_id:
                                vl_object.sudo().write({
                                    'unit_cost': line.product_id.standard_price_bali,
                                    'value': price
                                
                                })
                            else:
                                stock_move_obj = self.env['stock.move'].search([('id','=',line._origin.id)])
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
                                move_id = move_obj.sudo().create({
                                    'ref':str(self.name)+' - '+line.product_id.name,
                                    'date':lines.create_date,
                                    'journal_id':6,
                                    'line_ids': move_lines,
                                    'branch_id':self.branch_id.id,
                                    'stock_move_id':line._origin.id
                                })
                                vl_object.sudo().write({
                                    'unit_cost': line.product_id.standard_price_bali,
                                    'value': price,
                                    'account_move_id':move_id.id,
                                    'branch_id':line.branch_id
                                
                                })
                                move_id.sudo().post()
                    else:
                        continue
    def create_svl_transfer(self):
        print('test_print_3')
        svl_obj = self.env['stock.valuation.layer']
        move_obj = self.env['account.move']
        print('test_print_2')
        for i in self:
            for line in i.move_line_ids_without_package:
                if line.location_id.branch_id.id == 1:
                    if line.location_dest_id.branch_id.id != 1:
                        move_lines_journal= [
                        (0, 0, {
                            'account_id':line.product_id.categ_id.property_account_persediaan_transfer_jakarta_categ_id.id,
                            'name': str(self._origin.name)+' - '+line.product_id.name,
                            'credit':line.product_id.standard_price_jakarta*line.qty_done,
                            'currency_id':i.company_id.currency_id.id,
                        }),
                        (0, 0, {
                            'account_id':line.product_id.categ_id.property_account_rkcabang_categ_id.id,
                            'name': str(self._origin.name)+' - '+line.product_id.name,
                            'debit':line.product_id.standard_price_jakarta*line.qty_done,
                            'currency_id':i.company_id.currency_id.id,
                        }),
                        ]
                        move_id = move_obj.sudo().create({
                            'ref':str(self._origin.name)+' - '+line.product_id.name,
                            'date':i.create_date,
                            'journal_id':6,
                            'line_ids': move_lines_journal,
                            'branch_id':line.location_id.branch_id.id,
                            'stock_move_id':line.move_id.id
                        })
                        move_id.sudo().post()
                    svl_obj.sudo().create({
                        'create_date':line.create_date,
                        'product_id': line.product_id.id,
                        'quantity': line.qty_done*-1,
                        'uom_id':line.product_uom_id.id,
                        'unit_cost':line.product_id.standard_price_jakarta,
                        'value':line.product_id.standard_price_jakarta*line.qty_done*-1,
                        'description':str(self.name)+' - '+line.product_id.name,
                        'company_id': line.company_id.id,
                        'stock_move_id':line.move_id.id,
                        'branch_id': line.location_id.branch_id.id,
                    })
                    if  line.location_dest_id.branch_id.id == 2:
                        move_lines_journal= [
                        (0, 0, {
                            'account_id':line.product_id.categ_id.property_account_rkho_categ_id.id,
                            'name': str(self._origin.name)+' - '+line.product_id.name,
                            'credit':line.product_id.standard_price_jakarta*line.qty_done,
                            'currency_id':i.company_id.currency_id.id,
                        }),
                        (0, 0, {
                            'account_id':line.product_id.categ_id.property_account_persediaan_transfer_jakarta_categ_id.id,
                            'name': str(self._origin.name)+' - '+line.product_id.name,
                            'debit':line.product_id.standard_price_jakarta*line.qty_done,
                            'currency_id':i.company_id.currency_id.id,
                        }),
                        ]
                        move_id = move_obj.sudo().create({
                            'ref':str(self._origin.name)+' - '+line.product_id.name,
                            'date':i.create_date,
                            'journal_id':6,
                            'line_ids': move_lines_journal,
                            'branch_id':line.location_dest_id.branch_id.id,
                            'stock_move_id':line.move_id.id
                        })
                        move_id.sudo().post()
                        svl_obj.sudo().create({
                            'create_date':line.create_date,
                            'product_id': line.product_id.id,
                            'quantity': line.qty_done*1,
                            'uom_id':line.product_uom_id.id,
                            'unit_cost':line.product_id.standard_price_jakarta,
                            'value':line.product_id.standard_price_jakarta*line.qty_done*1,
                            'description':str(self.name)+' - '+line.product_id.name,
                            'company_id': line.company_id.id,
                            'stock_move_id':line.move_id.id,
                            # 'account_move_id':move_id.id,
                            'branch_id': line.location_dest_id.branch_id.id,
                        })
                    elif  line.location_dest_id.branch_id.id == 3:
                        move_lines_journal= [
                        (0, 0, {
                            'account_id':line.product_id.categ_id.property_account_rkho_categ_id.id,
                            'name': str(self._origin.name)+' - '+line.product_id.name,
                            'credit':line.product_id.standard_price_jakarta*line.qty_done,
                            'currency_id':i.company_id.currency_id.id,
                        }),
                        (0, 0, {
                            'account_id':line.product_id.categ_id.property_account_persediaan_transfer_jakarta_categ_id.id,
                            'name': str(self._origin.name)+' - '+line.product_id.name,
                            'debit':line.product_id.standard_price_jakarta*line.qty_done,
                            'currency_id':i.company_id.currency_id.id,
                        }),
                        ]
                        move_id = move_obj.sudo().create({
                            'ref':str(self._origin.name)+' - '+line.product_id.name,
                            'date':i.create_date,
                            'journal_id':6,
                            'line_ids': move_lines_journal,
                            'branch_id':line.location_dest_id.branch_id.id,
                            'stock_move_id':line.move_id.id
                        })
                        move_id.sudo().post()
                        svl_obj.sudo().create({
                            'create_date':line.create_date,
                            'product_id': line.product_id.id,
                            'quantity': line.qty_done*1,
                            'uom_id':line.product_uom_id.id,
                            'unit_cost':line.product_id.standard_price_jakarta,
                            'value':line.product_id.standard_price_jakarta*line.qty_done*1,
                            'description':str(self.name)+' - '+line.product_id.name,
                            'company_id': line.company_id.id,
                            'stock_move_id':line.move_id.id,
                            'account_move_id':move_id.id,
                            'branch_id': line.location_dest_id.branch_id.id,
                        })
                    elif  line.location_dest_id.branch_id.id == 1:
                        svl_obj.sudo().create({
                            'create_date':line.create_date,
                            'product_id': line.product_id.id,
                            'quantity': line.qty_done*1,
                            'uom_id':line.product_uom_id.id,
                            'unit_cost':line.product_id.standard_price_jakarta,
                            'value':line.product_id.standard_price_jakarta*line.qty_done*1,
                            'description':str(self.name)+' - '+line.product_id.name,
                            'company_id': line.company_id.id,
                            'stock_move_id':line.move_id.id,
                            'branch_id': line.location_dest_id.branch_id.id,
                        })
                elif line.location_id.branch_id.id == 2:
                    if line.location_dest_id.branch_id.id != 2:

                        move_lines_journal= [
                        (0, 0, {
                            'account_id':line.product_id.categ_id.property_account_persediaan_transfer_jakarta_categ_id.id,
                            'name': str(self._origin.name)+' - '+line.product_id.name,
                            'credit':line.product_id.standard_price_surabaya*line.qty_done,
                            'currency_id':i.company_id.currency_id.id,
                        }),
                        (0, 0, {
                            'account_id':line.product_id.categ_id.property_account_rkho_categ_id.id,
                            'name': str(self._origin.name)+' - '+line.product_id.name,
                            'debit':line.product_id.standard_price_surabaya*line.qty_done,
                            'currency_id':i.company_id.currency_id.id,
                        }),
                        ]
                        move_id = move_obj.sudo().create({
                            'ref':str(self._origin.name)+' - '+line.product_id.name,
                            'date':i.create_date,
                            'journal_id':6,
                            'line_ids': move_lines_journal,
                            'branch_id':line.location_id.branch_id.id,
                            'stock_move_id':line.move_id.id
                        })
                        move_id.sudo().post()
                    svl_obj.sudo().create({
                        'create_date':line.create_date,
                        'product_id': line.product_id.id,
                        'quantity': line.qty_done*-1,
                        'uom_id':line.product_uom_id.id,
                        'unit_cost':line.product_id.standard_price_surabaya,
                        'value':line.product_id.standard_price_surabaya*line.qty_done*-1,
                        'description':str(self.name)+' - '+line.product_id.name,
                        'company_id': line.company_id.id,
                        'stock_move_id':line.move_id.id,
                        'branch_id': line.location_id.branch_id.id,
                        # 'account_move_id':move_id.id,
                    })
                    if  line.location_dest_id.branch_id.id == 1:
                        move_lines_journal= [
                        (0, 0, {
                            'account_id':line.product_id.categ_id.property_account_rkcabang_categ_id.id,
                            'name': str(self._origin.name)+' - '+line.product_id.name,
                            'credit':line.product_id.standard_price_surabaya*line.qty_done,
                            'currency_id':i.company_id.currency_id.id,
                        }),
                        (0, 0, {
                            'account_id':line.product_id.categ_id.property_account_persediaan_transfer_jakarta_categ_id.id,
                            'name': str(self._origin.name)+' - '+line.product_id.name,
                            'debit':line.product_id.standard_price_surabaya*line.qty_done,
                            'currency_id':i.company_id.currency_id.id,
                        }),
                        ]
                        move_id = move_obj.sudo().create({
                            'ref':str(self._origin.name)+' - '+line.product_id.name,
                            'date':i.create_date,
                            'journal_id':6,
                            'line_ids': move_lines_journal,
                            'branch_id':line.location_dest_id.branch_id.id,
                            'stock_move_id':line.move_id.id
                        })
                        move_id.sudo().post()
                        svl_obj.sudo().create({
                            'create_date':line.create_date,
                            'product_id': line.product_id.id,
                            'quantity': line.qty_done*1,
                            'uom_id':line.product_uom_id.id,
                            'unit_cost':line.product_id.standard_price_surabaya,
                            'value':line.product_id.standard_price_surabaya*line.qty_done*1,
                            'description':str(self.name)+' - '+line.product_id.name,
                            'company_id': line.company_id.id,
                            'stock_move_id':line.move_id.id,
                            'branch_id': line.location_dest_id.branch_id.id,
                            'account_move_id':move_id.id,
                        })
                    elif  line.location_dest_id.branch_id.id == 3:
                        move_lines_journal= [
                        (0, 0, {
                            'account_id':line.product_id.categ_id.property_account_rkho_categ_id.id,
                            'name': str(self._origin.name)+' - '+line.product_id.name,
                            'credit':line.product_id.standard_price_surabaya*line.qty_done,
                            'currency_id':i.company_id.currency_id.id,
                        }),
                        (0, 0, {
                            'account_id':line.product_id.categ_id.property_account_persediaan_transfer_jakarta_categ_id.id,
                            'name': str(self._origin.name)+' - '+line.product_id.name,
                            'debit':line.product_id.standard_price_surabaya*line.qty_done,
                            'currency_id':i.company_id.currency_id.id,
                        }),
                        ]
                        move_id = move_obj.sudo().create({
                            'ref':str(self._origin.name)+' - '+line.product_id.name,
                            'date':i.create_date,
                            'journal_id':6,
                            'line_ids': move_lines_journal,
                            'branch_id':line.location_dest_id.branch_id.id,
                            'stock_move_id':line.move_id.id
                        })
                        move_id.sudo().post()
                        svl_obj.sudo().create({
                            'create_date':line.create_date,
                            'product_id': line.product_id.id,
                            'quantity': line.qty_done*1,
                            'uom_id':line.product_uom_id.id,
                            'unit_cost':line.product_id.standard_price_surabaya,
                            'value':line.product_id.standard_price_surabaya*line.qty_done*1,
                            'description':str(self.name)+' - '+line.product_id.name,
                            'company_id': line.company_id.id,
                            'stock_move_id':line.move_id.id,
                            'branch_id': line.location_dest_id.branch_id.id,
                            'account_move_id':move_id.id,
                        })
                    elif  line.location_dest_id.branch_id.id == 2:
                        svl_obj.sudo().create({
                            'create_date':line.create_date,
                            'product_id': line.product_id.id,
                            'quantity': line.qty_done*1,
                            'uom_id':line.product_uom_id.id,
                            'unit_cost':line.product_id.standard_price_surabaya,
                            'value':line.product_id.standard_price_surabaya*line.qty_done*1,
                            'description':str(self.name)+' - '+line.product_id.name,
                            'company_id': line.company_id.id,
                            'stock_move_id':line.move_id.id,
                            'branch_id': line.location_dest_id.branch_id.id,
                        })
                elif line.location_id.branch_id.id == 3:
                    if line.location_dest_id.branch_id.id != 3:
                        move_lines_journal= [
                        (0, 0, {
                            'account_id':line.product_id.categ_id.property_account_persediaan_transfer_jakarta_categ_id.id,
                            'name': str(self._origin.name)+' - '+line.product_id.name,
                            'credit':line.product_id.standard_price_bali*line.qty_done,
                            'currency_id':i.company_id.currency_id.id,
                        }),
                        (0, 0, {
                            'account_id':line.product_id.categ_id.property_account_rkho_categ_id.id,
                            'name': str(self._origin.name)+' - '+line.product_id.name,
                            'debit':line.product_id.standard_price_bali*line.qty_done,
                            'currency_id':i.company_id.currency_id.id,
                        }),
                        ]
                        move_id = move_obj.sudo().create({
                            'ref':str(self._origin.name)+' - '+line.product_id.name,
                            'date':i.create_date,
                            'journal_id':6,
                            'line_ids': move_lines_journal,
                            'branch_id':line.location_id.branch_id.id,
                            'stock_move_id':line.move_id.id
                        })
                        move_id.sudo().post()
                    svl_obj.sudo().create({
                        'create_date':line.create_date,
                        'product_id': line.product_id.id,
                        'quantity': line.qty_done*-1,
                        'uom_id':line.product_uom_id.id,
                        'unit_cost':line.product_id.standard_price_bali,
                        'value':line.product_id.standard_price_bali*line.qty_done*-1,
                        'description':str(self.name)+' - '+line.product_id.name,
                        'company_id': line.company_id.id,
                        'stock_move_id':line.move_id.id,
                        'branch_id': line.location_id.branch_id.id,
                        # 'account_move_id':move_id.id,
                    })
                    if  line.location_dest_id.branch_id.id == 1:

                        move_lines_journal= [
                        (0, 0, {
                            'account_id':line.product_id.categ_id.property_account_rkcabang_categ_id.id,
                            'name': str(self._origin.name)+' - '+line.product_id.name,
                            'credit':line.product_id.standard_price_bali*line.qty_done,
                            'currency_id':i.company_id.currency_id.id,
                        }),
                        (0, 0, {
                            'account_id':line.product_id.categ_id.property_account_persediaan_transfer_jakarta_categ_id.id,
                            'name': str(self._origin.name)+' - '+line.product_id.name,
                            'debit':line.product_id.standard_price_bali*line.qty_done,
                            'currency_id':i.company_id.currency_id.id,
                        }),
                        ]
                        move_id = move_obj.sudo().create({
                            'ref':str(self._origin.name)+' - '+line.product_id.name,
                            'date':i.create_date,
                            'journal_id':6,
                            'line_ids': move_lines_journal,
                            'branch_id':line.location_dest_id.branch_id.id,
                            'stock_move_id':line.move_id.id
                        })
                        move_id.sudo().post()
                        svl_obj.sudo().create({
                            'create_date':line.create_date,
                            'product_id': line.product_id.id,
                            'quantity': line.qty_done*1,
                            'uom_id':line.product_uom_id.id,
                            'unit_cost':line.product_id.standard_price_bali,
                            'value':line.product_id.standard_price_bali*line.qty_done*1,
                            'description':str(self.name)+' - '+line.product_id.name,
                            'company_id': line.company_id.id,
                            'stock_move_id':line.move_id.id,
                            'branch_id': line.location_dest_id.branch_id.id,
                            'account_move_id':move_id.id,
                        })
                    elif  line.location_dest_id.branch_id.id == 3:
                        svl_obj.sudo().create({
                            'create_date':line.create_date,
                            'product_id': line.product_id.id,
                            'quantity': line.qty_done*1,
                            'uom_id':line.product_uom_id.id,
                            'unit_cost':line.product_id.standard_price_bali,
                            'value':line.product_id.standard_price_bali*line.qty_done*1,
                            'description':str(self.name)+' - '+line.product_id.name,
                            'company_id': line.company_id.id,
                            'stock_move_id':line.move_id.id,
                            'branch_id': line.location_dest_id.branch_id.id,
                        })
                    elif  line.location_dest_id.branch_id.id == 2:
                        move_lines_journal= [
                        (0, 0, {
                            'account_id':line.product_id.categ_id.property_account_rkho_categ_id.id,
                            'name': str(self._origin.name)+' - '+line.product_id.name,
                            'credit':line.product_id.standard_price_bali*line.qty_done,
                            'currency_id':i.company_id.currency_id.id,
                        }),
                        (0, 0, {
                            'account_id':line.product_id.categ_id.property_account_persediaan_transfer_jakarta_categ_id.id,
                            'name': str(self._origin.name)+' - '+line.product_id.name,
                            'debit':line.product_id.standard_price_bali*line.qty_done,
                            'currency_id':i.company_id.currency_id.id,
                        }),
                        ]
                        move_id = move_obj.sudo().create({
                            'ref':str(self._origin.name)+' - '+line.product_id.name,
                            'date':i.create_date,
                            'journal_id':6,
                            'line_ids': move_lines_journal,
                            'branch_id':line.location_dest_id.branch_id.id,
                            'stock_move_id':line.move_id.id
                        })
                        move_id.sudo().post()
                        svl_obj.sudo().create({
                            'create_date':line.create_date,
                            'product_id': line.product_id.id,
                            'quantity': line.qty_done*1,
                            'uom_id':line.product_uom_id.id,
                            'unit_cost':line.product_id.standard_price_bali,
                            'value':line.product_id.standard_price_bali*line.qty_done*1,
                            'description':str(self.name)+' - '+line.product_id.name,
                            'company_id': line.company_id.id,
                            'stock_move_id':line.move_id.id,
                            'account_move_id':move_id.id,
                            'branch_id': line.location_dest_id.branch_id.id,
                        })
                else:
                    continue
    def update_valuation_purchase(self):
        print('test_print_purchase')
        for this in self:
            for line in this.move_lines:
                vl_object= self.env['stock.valuation.layer'].sudo().search([('stock_move_id','=',line._origin.id)])
                for lines in line.stock_valuation_layer_ids:
                    vl_object.sudo().write({
                                'branch_id':line.branch_id     
                            })
                print(this.location_dest_id.branch_id.id,'this_branc_id')
                if this.location_id.branch_id.id == False:
                    if this.location_dest_id.branch_id.id == 1:
                        for lines in line.stock_valuation_layer_ids:
                            vl_object.sudo().write({
                                        'branch_id':line.branch_id,
                                    })
                            move_id = vl_object.stock_move_id.account_move_ids
                            move_id.sudo().write({
                                'branch_id':line.branch_id,
                            })
                            print(vl_object.stock_move_id.account_move_ids,'test_account_id')
                    if this.location_dest_id.branch_id.id == 2:
                        for lines in line.stock_valuation_layer_ids:
                            vl_object.sudo().write({
                                        'branch_id':line.branch_id,
                                    })
                            move_id = vl_object.stock_move_id.account_move_ids
                            move_id.sudo().write({
                                'branch_id':line.branch_id,
                            })
                    if this.location_dest_id.branch_id.id == 3:
                        for lines in line.stock_valuation_layer_ids:
                            vl_object.sudo().write({
                                        'branch_id':line.branch_id,
                                    })
                            move_id = vl_object.stock_move_id.account_move_ids
                            move_id.sudo().write({
                                'branch_id':line.branch_id,
                            })


    def button_detect(self):
        for lines in self:
            if lines.tanggal_diterima:
               continue
            else:
                raise UserError(('Tolong Tanggal Diterimanya Di isi'))
                    

    def _action_done(self):
        print('action_button',self.picking_type_code)
        self.button_detect()
        if self.picking_type_code == 'internal':
            if self.product_id.cost_method == 'branch':
                self.create_svl_transfer()
                self.update_stock()
        res =  super(StockPicking, self)._action_done()

        if self.picking_type_code == 'outgoing':
            self.update_valuation()
            print('action_button',self.picking_type_code)
        
        elif self.picking_type_code == 'incoming':
            self.update_valuation_purchase()
            print('action_button',self.picking_type_code)

        return res

    def perbaikan_kurang(self):
        all_id = self.env['stock.picking'].search([('picking_type_code','=','internal')])
        svl_obj = self.env['stock.valuation.layer']
        
        for i in all_id:
            for line in i.move_line_ids_without_package:
                if line.location_id.branch_id.id == line.location_dest_id.branch_id.id:
                    svl_obj_value = self.env['stock.valuation.layer'].search([('stock_move_id','=',line.move_id.id)])
                    for lines in svl_obj_value:
                        svl_obj.sudo().create({
                                'create_date':line.create_date,
                                'product_id': line.product_id.id,
                                'quantity': line.qty_done*1,
                                'uom_id':line.product_uom_id.id,
                                'unit_cost':lines.unit_cost,
                                'value':lines.value*-1,
                                'description':str(self.name)+' - '+line.product_id.name,
                                'company_id': line.company_id.id,
                                'stock_move_id':line.move_id.id,
                                'branch_id': line.location_dest_id.branch_id.id,
                            })

    def create_journal_perbaikan(self):
        all_id = self.env['stock.picking'].search([('picking_type_code','=','internal')])
        move_obj = self.env['account.move']

        for i in all_id:
            for line in i.move_line_ids_without_package:
                 svl_obj_value = self.env['stock.valuation.layer'].search([('stock_move_id','=',line.move_id.id)])
                 for lines in svl_obj_value:
                    if lines.branch_id.id == 1 and line.location_dest_id.branch_id.id != 1:
                        if lines.value >0:
                            move_lines_journal= [
                            (0, 0, {
                                'account_id':line.product_id.categ_id.property_account_rkho_categ_id.id,
                                'name': str(i._origin.name)+' - '+line.product_id.name,
                                'credit':abs(lines.value),
                                'currency_id':line.company_id.currency_id.id,
                            }),
                            (0, 0, {
                                'account_id':line.product_id.categ_id.property_account_persediaan_transfer_jakarta_categ_id.id,
                                'name': str(i._origin.name)+' - '+line.product_id.name,
                                'debit':abs(lines.value),
                                'currency_id':line.company_id.currency_id.id,
                            }),
                            ]
                            move_id = move_obj.sudo().create({
                                'ref':str(i._origin.name)+' - '+line.product_id.name,
                                'date':line.create_date,
                                'journal_id':6,
                                'line_ids': move_lines_journal,
                                'branch_id':lines.branch_id.id,
                                'stock_move_id':line.move_id.id
                            })
                            move_id.sudo().post()
                        if lines.value <0:
                            move_lines_journal= [
                            (0, 0, {
                                'account_id':line.product_id.categ_id.property_account_persediaan_transfer_jakarta_categ_id.id,
                                'name': str(i._origin.name)+' - '+line.product_id.name,
                                'credit':abs(lines.value),
                                'currency_id':line.company_id.currency_id.id,
                            }),
                            (0, 0, {
                                'account_id':line.product_id.categ_id.property_account_rkcabang_categ_id.id,
                                'name': str(i._origin.name)+' - '+line.product_id.name,
                                'debit':abs(lines.value),
                                'currency_id':line.company_id.currency_id.id,
                            }),
                            ]
                            move_id = move_obj.sudo().create({
                                'ref':str(i._origin.name)+' - '+line.product_id.name,
                                'date':line.create_date,
                                'journal_id':6,
                                'line_ids': move_lines_journal,
                                'branch_id':lines.branch_id.id,
                                'stock_move_id':line.move_id.id
                            })
                            move_id.sudo().post()
                    if lines.branch_id.id != 1 and line.location_dest_id.branch_id.id == 1:

                        move_lines_journal= [
                        (0, 0, {
                            'account_id':line.product_id.categ_id.property_account_rkcabang_categ_id.id,
                            'name': str(i._origin.name)+' - '+line.product_id.name,
                            'credit':abs(lines.value),
                            'currency_id':line.company_id.currency_id.id,
                        }),
                        (0, 0, {
                            'account_id':line.product_id.categ_id.property_account_persediaan_transfer_jakarta_categ_id.id,
                            'name': str(i._origin.name)+' - '+line.product_id.name,
                            'debit':abs(lines.value),
                            'currency_id':line.company_id.currency_id.id,
                        }),
                        ]
                        move_id = move_obj.sudo().create({
                            'ref':str(i._origin.name)+' - '+line.product_id.name,
                            'date':line.create_date,
                            'journal_id':6,
                            'line_ids': move_lines_journal,
                            'branch_id':lines.branch_id.id,
                            'stock_move_id':line.move_id.id
                        })
                        move_id.sudo().post()
                        
                        
                    if lines.branch_id.id != 1 and line.location_dest_id.branch_id.id != 1:
                        move_lines_journal= [
                        (0, 0, {
                            'account_id':line.product_id.categ_id.property_account_rkho_categ_id.id,
                            'name': str(i._origin.name)+' - '+line.product_id.name,
                            'credit':abs(lines.value),
                            'currency_id':line.company_id.currency_id.id,
                        }),
                        (0, 0, {
                            'account_id':line.product_id.categ_id.property_account_persediaan_transfer_jakarta_categ_id.id,
                            'name': str(i._origin.name)+' - '+line.product_id.name,
                            'debit':abs(lines.value),
                            'currency_id':line.company_id.currency_id.id,
                        }),
                        ]
                        move_id = move_obj.sudo().create({
                            'ref':str(i._origin.name)+' - '+line.product_id.name,
                            'date':line.create_date,
                            'journal_id':6,
                            'line_ids': move_lines_journal,
                            'branch_id':lines.branch_id.id,
                            'stock_move_id':line.move_id.id
                        })
                        move_id.sudo().post()
                  