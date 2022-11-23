
from ast import Store
import datetime
import string
from odoo import models, fields, api,_
from dateutil.relativedelta import relativedelta
from datetime import datetime,timedelta
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    user_branch_ids = fields.Many2many('res.branch', compute="get_default_branch",store=True)
    
    
    def get_default_branch(self):
        """methode to get branch domain"""
        company = self.env.company
        branch_ids = self.env.user.branch_ids.ids

        self.user_branch_ids= branch_ids
    

            

  