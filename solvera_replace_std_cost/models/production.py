
import datetime
from itertools import product
from shutil import move
import string
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime,timedelta

class MrpProduction(models.Model):
    _inherit = 'mrp.production'
   
    field_coba = fields.Date()
    
    def journal_branch(self):
        temp=0
        price_temp=0
        
        if self.location_src_id.branch_id.id == 1:
            for this in self.move_raw_ids:
                vl_object = self.env['stock.valuation.layer'].search([('stock_move_id','=',this._origin.id)])
                price = this.product_id.standard_price_jakarta
                move_obj=self.env['account.move']
                if vl_object.account_move_id:
                    vl_object.sudo().write({
                        'unit_cost': this.product_id.standard_price_jakarta,
                        'value': price*vl_object.quantity,
                        'branch_id':self.location_src_id.branch_id.id
                    
                    })
                    account_move_obj = self.env['account.move'].search([('id','=',vl_object.account_move_id.id)])
                    move_lines_journal = [
                    (0, 0, {
                      
                        'credit':price*vl_object.quantity*-1,
                        'currency_id':self.company_id.currency_id.id,

                    }),
                    (0, 0, {
                        
                        'debit':price*vl_object.quantity*-1,
                        'currency_id':self.company_id.currency_id.id,

                    }),
                    ]
                    account_move_obj.sudo().update({
                    'line_ids': move_lines_journal,
                    })
                else:
                    move_lines = [
                    (0, 0, {
                        'account_id':this.product_id.categ_id.property_account_input_production_categ_id.id,
                        'name': str(self._origin.name)+' - '+this.product_id.name,
                        'credit':price*vl_object.quantity*-1,
                        'currency_id':this.company_id.currency_id.id,
                    }),
                    (0, 0, {
                        'account_id':this.product_id.categ_id.property_account_output_production_categ_id.id,
                        'name': str(self._origin.name)+' - '+this.product_id.name,
                        'debit':price*vl_object.quantity*-1,
                        'currency_id':this.company_id.currency_id.id,
                    }),
                    ]
                    move_id = move_obj.create({
                        'ref':str(self._origin.name)+' - '+this.product_id.name,
                        'date':this.create_date,
                        'journal_id':6,
                        'line_ids': move_lines,
                        'branch_id':self.location_src_id.branch_id.id,
                        'stock_move_id':this._origin.id
                    })
                    vl_object.sudo().write({
                        'unit_cost': this.product_id.standard_price_surabaya,
                        'value': price*vl_object.quantity,
                        'account_move_id':move_id.id,
                        'branch_id':self.location_src_id.branch_id.id,
                    
                    })
                    move_id.post()
                    stock_move = self.env['stock.move'].search([('id','=',this._origin.id)])
                    stock_move.write({
                        'branch_id':self.location_src_id.branch_id.id,
                    
                    })
                temp = temp+vl_object.value



            for i in self.move_finished_ids:
                
                vl_object_finish = self.env['stock.valuation.layer'].search([('stock_move_id','=',i._origin.id)])
                price_finish =temp*-1
                if i.product_id.standard_price_jakarta == 0:
                    price_temp=price_temp*0
                    i.product_id.standard_price_jakarta = price_finish/vl_object_finish.quantity
                    price_temp=price_temp+1
                move_obj_finish=self.env['account.move']
                if vl_object_finish.account_move_id:
                    vl_object_finish.sudo().write({
                        'unit_cost': i.product_id.standard_price_jakarta,
                        'value': price_finish*vl_object_finish.quantity,
                        'branch_id':self.branch_id.id
                    
                    })
                else:
                    move_lines_journal_finished = [
                    (0, 0, {
                        'account_id':i.product_id.categ_id.property_account_output_production_categ_id.id,
                        'name': str(self._origin.name)+' - '+i.product_id.name,
                        'credit':price_finish,
                        'currency_id':this.company_id.currency_id.id,
                    }),
                    (0, 0, {
                        'account_id':i.product_id.categ_id.property_account_input_production_categ_id.id,
                        'name': str(self._origin.name)+' - '+i.product_id.name,
                        'debit':price_finish,
                        'currency_id':i.company_id.currency_id.id,
                    }),
                    ]
                    move_id_finished = move_obj_finish.create({
                        'ref':str(self._origin.name)+' - '+i.product_id.name,
                        'date':i.create_date,
                        'journal_id':6,
                        'line_ids': move_lines_journal_finished,
                        'branch_id':self.location_src_id.branch_id.id,
                        'stock_move_id':i._origin.id
                    })
                    vl_object_finish.sudo().write({
                        'unit_cost': price_finish/vl_object_finish.quantity,
                        'value': price_finish,
                        'account_move_id':move_id_finished.id,
                        'branch_id':self.location_src_id.branch_id.id
                    
                    })
                    move_id_finished.post()
                    stock_move_finish = self.env['stock.move'].search([('id','=',i._origin.id)])
                    stock_move_finish.write({
                        'branch_id':self.location_src_id.branch_id.id,
                    
                    })
                    for line in i.product_id.stock_quant_ids:
                        if price_temp ==0:
                            for product in i.location_dest_id.quant_ids:
                                if i.product_id.default_code == product.product_id.default_code :
                                    act_quant = round(product.quantity,0) - round(vl_object_finish.quantity,0)
                                    print(act_quant,'test_print1',line.quantity,product.product_id.name)
                                    if act_quant != 0:
                                        if line.location_id.branch_id.id == self.location_src_id.branch_id.id:
                                            print(act_quant,'test_print2',line.quantity)
                                            new_cost= ((i.product_id.standard_price_jakarta*act_quant)+price_finish)/(act_quant+vl_object_finish.quantity)
                                            i.product_id.standard_price_jakarta=new_cost
                                    elif act_quant == 0:
                                        if line.location_id.branch_id.id == self.location_src_id.branch_id.id:
                                            print(act_quant,'test_print3',line.quantity)
                                            i.product_id.standard_price_jakarta= price_finish/vl_object_finish.quantity
                        else:
                            for product in i.location_dest_id.quant_ids:
                                if i.product_id.default_code == product.product_id.default_code :
                                    act_quant = round(product.quantity,0) - round(vl_object_finish.quantity,0)
                                    if act_quant != 0:
                                        if line.location_id.branch_id.id == self.location_src_id.branch_id.id:
                                            new_cost= ((i.product_id.standard_price_jakarta*act_quant)+price_finish)/(act_quant+vl_object_finish.quantity)
                                            i.product_id.standard_price_jakarta=new_cost
                                    elif act_quant == 0:
                                        if line.location_id.branch_id.id == self.location_src_id.branch_id.id:
                                            i.product_id.standard_price_jakarta= price_finish/vl_object_finish.quantity








        if self.location_src_id.branch_id.id == 2:
            for this in self.move_raw_ids:
                vl_object = self.env['stock.valuation.layer'].search([('stock_move_id','=',this._origin.id)])
                price = this.product_id.standard_price_surabaya
                move_obj=self.env['account.move']
                if vl_object.account_move_id:
                    vl_object.sudo().write({
                        'unit_cost': this.product_id.standard_price_surabaya,
                        'value': price*vl_object.quantity,
                        'branch_id':self.location_src_id.branch_id.id
                    
                    })
                else:
                    move_lines = [
                    (0, 0, {
                        'account_id':this.product_id.categ_id.property_account_input_production_categ_id.id,
                        'name': str(self._origin.name)+' - '+this.product_id.name,
                        'credit':price*vl_object.quantity*-1,
                        'currency_id':this.company_id.currency_id.id,
                    }),
                    (0, 0, {
                        'account_id':this.product_id.categ_id.property_account_output_production_categ_id.id,
                        'name': str(self._origin.name)+' - '+this.product_id.name,
                        'debit':price*vl_object.quantity*-1,
                        'currency_id':this.company_id.currency_id.id,
                    }),
                    ]
                    move_id = move_obj.create({
                        'ref':str(self._origin.name)+' - '+this.product_id.name,
                        'date':this.create_date,
                        'journal_id':6,
                        'line_ids': move_lines,
                        'branch_id':self.location_src_id.branch_id.id,
                        'stock_move_id':this._origin.id
                    })
                    vl_object.sudo().write({
                        'unit_cost': this.product_id.standard_price_surabaya,
                        'value': price*vl_object.quantity,
                        'account_move_id':move_id.id,
                        'branch_id':self.location_src_id.branch_id.id
                    
                    })
                    move_id.post()
                    stock_move = self.env['stock.move'].search([('id','=',this._origin.id)])
                    stock_move.write({
                        'branch_id':self.location_src_id.branch_id.id,
                    
                    })
                temp = temp+vl_object.value



            for i in self.move_finished_ids:
                vl_object_finish = self.env['stock.valuation.layer'].search([('stock_move_id','=',i._origin.id)])
                price_finish =temp*-1
                if i.product_id.standard_price_surabaya == 0:
                    price_temp=price_temp*0
                    i.product_id.standard_price_surabaya = price_finish/vl_object_finish.quantity
                    price_temp=price_temp+1
                move_obj_finish=self.env['account.move']
                if vl_object_finish.account_move_id:
                    vl_object_finish.sudo().write({
                        'unit_cost': i.product_id.standard_price_surabaya,
                        'value': price_finish*vl_object_finish.quantity,
                        'branch_id':self.location_src_id.branch_id.id
                    
                    })
                else:
                    move_lines_journal_finished = [
                    (0, 0, {
                        'account_id':i.product_id.categ_id.property_account_output_production_categ_id.id,
                        'name': str(self._origin.name)+' - '+i.product_id.name,
                        'credit':price_finish,
                        'currency_id':this.company_id.currency_id.id,
                    }),
                    (0, 0, {
                        'account_id':i.product_id.categ_id.property_account_input_production_categ_id.id,
                        'name': str(self._origin.name)+' - '+i.product_id.name,
                        'debit':price_finish,
                        'currency_id':i.company_id.currency_id.id,
                    }),
                    ]
                    move_id_finished = move_obj_finish.create({
                        'ref':str(self._origin.name)+' - '+i.product_id.name,
                        'date':i.create_date,
                        'journal_id':6,
                        'line_ids': move_lines_journal_finished,
                        'branch_id':self.location_src_id.branch_id.id,
                        'stock_move_id':i._origin.id
                    })
                    vl_object_finish.sudo().write({
                        'unit_cost': price_finish/vl_object_finish.quantity,
                        'value': price_finish,
                        'account_move_id':move_id_finished.id,
                        'branch_id':self.location_src_id.branch_id.id
                    
                    })
                    move_id_finished.post()
                    stock_move_finish = self.env['stock.move'].search([('id','=',i._origin.id)])
                    stock_move_finish.write({
                        'branch_id':self.location_src_id.branch_id.id,
                    
                    })
                    for line in i.product_id.stock_quant_ids:
                        # if price_temp==0:
                        #     if line.location_id.branch_id.id == self.location_src_id.branch_id.id:
                        #         new_cost= ((i.product_id.standard_price_surabaya*line.quantity)+price_finish)/(line.quantity+vl_object_finish.quantity)
                        #         i.product_id.standard_price_surabaya=new_cost
                        if price_temp ==0:
                            for product in i.location_dest_id.quant_ids:
                                if i.product_id.default_code == product.product_id.default_code :
                                    act_quant = round(product.quantity,0) - round(vl_object_finish.quantity,0)
                                    print(act_quant,'test_print1',line.quantity)
                                    if act_quant != 0:
                                        if line.location_id.branch_id.id == self.location_src_id.branch_id.id:
                                            print(act_quant,'test_print2',line.quantity)
                                            new_cost= ((i.product_id.standard_price_surabaya*act_quant)+price_finish)/(act_quant+vl_object_finish.quantity)
                                            i.product_id.standard_price_surabaya=new_cost
                                    elif act_quant == 0:
                                        if line.location_id.branch_id.id == self.location_src_id.branch_id.id:
                                            print(act_quant,'test_print3',line.quantity)
                                            i.product_id.standard_price_surabaya= price_finish/vl_object_finish.quantity
                        else:
                            for product in i.location_dest_id.quant_ids:
                                if i.product_id.default_code == product.product_id.default_code :
                                    act_quant = round(product.quantity,0) - round(vl_object_finish.quantity,0)
                                    if act_quant != 0:
                                        if line.location_id.branch_id.id == self.location_src_id.branch_id.id:
                                            new_cost= ((i.product_id.standard_price_surabaya*act_quant)+price_finish)/(act_quant+vl_object_finish.quantity)
                                            i.product_id.standard_price_surabaya=new_cost
                                    elif act_quant == 0:
                                        if line.location_id.branch_id.id == self.location_src_id.branch_id.id:
                                            i.product_id.standard_price_surabaya= price_finish/vl_object_finish.quantity










        if self.location_src_id.branch_id.id == 3:
            for this in self.move_raw_ids:
                vl_object = self.env['stock.valuation.layer'].search([('stock_move_id','=',this._origin.id)])
                price = this.product_id.standard_price_bali
                move_obj=self.env['account.move']
                if vl_object.account_move_id:
                    vl_object.sudo().write({
                        'unit_cost': this.product_id.standard_price_bali,
                        'value': price*vl_object.quantity,
                        'branch_id':self.location_src_id.branch_id.id
                    
                    })
             
                else:
                    move_lines = [
                    (0, 0, {
                        'account_id':this.product_id.categ_id.property_account_input_production_categ_id.id,
                        'name': str(self._origin.name)+' - '+this.product_id.name,
                        'credit':price*vl_object.quantity*-1,
                        'currency_id':this.company_id.currency_id.id,
                    }),
                    (0, 0, {
                        'account_id':this.product_id.categ_id.property_account_output_production_categ_id.id,
                        'name': str(self._origin.name)+' - '+this.product_id.name,
                        'debit':price*vl_object.quantity*-1,
                        'currency_id':this.company_id.currency_id.id,
                    }),
                    ]
                    move_id = move_obj.create({
                        'ref':str(self._origin.name)+' - '+this.product_id.name,
                        'date':this.create_date,
                        'journal_id':6,
                        'line_ids': move_lines,
                        'branch_id':self.location_src_id.branch_id.id,
                        'stock_move_id':this._origin.id
                    })
                    vl_object.sudo().write({
                        'unit_cost': this.product_id.standard_price_bali,
                        'value': price*vl_object.quantity,
                        'account_move_id':move_id.id,
                        'branch_id':self.location_src_id.branch_id.id
                    
                    })
                    move_id.post()
                    stock_move = self.env['stock.move'].search([('id','=',this._origin.id)])
                    stock_move.write({
                        'branch_id':self.location_src_id.branch_id.id,
                    
                    })
                temp = temp+vl_object.value



            for i in self.move_finished_ids:
                vl_object_finish = self.env['stock.valuation.layer'].search([('stock_move_id','=',i._origin.id)])
                price_finish =temp*-1
                if i.product_id.standard_price_bali == 0:
                    price_temp=price_temp*0
                    i.product_id.standard_price_bali = price_finish/vl_object_finish.quantity
                    price_temp=price_temp+1
                move_obj_finish=self.env['account.move']
                if vl_object_finish.account_move_id:
                    vl_object_finish.sudo().write({
                        'unit_cost': i.product_id.standard_price_bali,
                        'value': price_finish*vl_object_finish.quantity,
                        'branch_id':self.location_src_id.branch_id.id
                    
                    })
                else:
                    move_lines_journal_finished = [
                    (0, 0, {
                        'account_id':i.product_id.categ_id.property_account_output_production_categ_id.id,
                        'name': str(self._origin.name)+' - '+i.product_id.name,
                        'credit':price_finish,
                        'currency_id':this.company_id.currency_id.id,
                    }),
                    (0, 0, {
                        'account_id':i.product_id.categ_id.property_account_input_production_categ_id.id,
                        'name': str(self._origin.name)+' - '+i.product_id.name,
                        'debit':price_finish,
                        'currency_id':i.company_id.currency_id.id,
                    }),
                    ]
                    move_id_finished = move_obj_finish.create({
                        'ref':str(self._origin.name)+' - '+i.product_id.name,
                        'date':i.create_date,
                        'journal_id':6,
                        'line_ids': move_lines_journal_finished,
                        'branch_id':self.location_src_id.branch_id.id,
                        'stock_move_id':i._origin.id
                    })
                    vl_object_finish.sudo().write({
                        'unit_cost': price_finish/vl_object_finish.quantity,
                        'value': price_finish,
                        'account_move_id':move_id_finished.id,
                        'branch_id':self.location_src_id.branch_id.id
                    
                    })
                    move_id_finished.post()
                    stock_move_finish = self.env['stock.move'].search([('id','=',i._origin.id)])
                    stock_move_finish.write({
                        'branch_id':self.location_src_id.branch_id.id,
                    
                    })
                    for line in i.product_id.stock_quant_ids:
                        # if price_temp==0:
                        #     if line.location_id.branch_id.id == self.location_src_id.branch_id.id:
                        #         new_cost= ((i.product_id.standard_price_bali*line.quantity)+price_finish)/(line.quantity+vl_object_finish.quantity)
                        #         i.product_id.standard_price_bali=new_cost

                        if price_temp ==0:
                            for product in i.location_dest_id.quant_ids:
                                if i.product_id.default_code == product.product_id.default_code :
                                    act_quant = round(product.quantity,0) - round(vl_object_finish.quantity,0)
                                    print(act_quant,'test_print1',line.quantity)
                                    if act_quant != 0:
                                        if line.location_id.branch_id.id == self.location_src_id.branch_id.id:
                                            print(act_quant,'test_print2',line.quantity)
                                            new_cost= ((i.product_id.standard_price_bali*act_quant)+price_finish)/(act_quant+vl_object_finish.quantity)
                                            i.product_id.standard_price_bali=new_cost
                                    elif act_quant == 0:
                                        if line.location_id.branch_id.id == self.location_src_id.branch_id.id:
                                            print(act_quant,'test_print3',line.quantity)
                                            i.product_id.standard_price_bali= price_finish/vl_object_finish.quantity
                        else:
                            for product in i.location_dest_id.quant_ids:
                                if i.product_id.default_code == product.product_id.default_code :
                                    act_quant = round(product.quantity,0) - round(vl_object_finish.quantity,0)
                                    if act_quant != 0:
                                        if line.location_id.branch_id.id == self.location_src_id.branch_id.id:
                                            new_cost= ((i.product_id.standard_price_bali*act_quant)+price_finish)/(act_quant+vl_object_finish.quantity)
                                            i.product_id.standard_price_bali=new_cost
                                    elif act_quant == 0:
                                        if line.location_id.branch_id.id == self.location_src_id.branch_id.id:
                                            i.product_id.standard_price_bali= price_finish/vl_object_finish.quantity


                            
        

    def button_mark_done(self):
        res=super(MrpProduction, self).button_mark_done()
        if self.qty_producing != 0:
            self.journal_branch()

        return res
    
    def perbaikan(self):
        all_id = self.env['mrp.production'].search([])
        
        for i in all_id:
            for line in i.move_finished_ids:
                if line.location_id.branch_id.id != 1:
                    for lines in line.account_move_ids:
                        for move in lines.line_ids:
                            if move.credit == 0:
                                move.update({
                                        'account_id': line.product_id.categ_id.property_account_input_production_categ_id.id,
                                    })
                            if move.debit == 0:
                                move.update({
                                        'account_id': line.product_id.categ_id.property_account_output_production_categ_id.id,
                                    })
            for line in i.move_raw_ids:
                if line.location_id.branch_id.id != 1:
                    for lines in line.account_move_ids:
                        for move in lines.line_ids:
                            if move.credit == 0:
                                move.update({
                                        'account_id': line.product_id.categ_id.property_account_output_production_categ_id.id,
                                    })
                            if move.debit == 0:
                                move.update({
                                        'account_id': line.product_id.categ_id.property_account_input_production_categ_id.id,
                                    })
