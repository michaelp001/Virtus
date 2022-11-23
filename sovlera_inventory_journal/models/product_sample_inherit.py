
from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
from odoo.tools import float_compare, date_utils, email_split, email_re
from odoo.tools.misc import formatLang, format_date, get_lang

from datetime import date, timedelta
from collections import defaultdict
from itertools import zip_longest
from hashlib import sha256
from json import dumps

import ast
import json
import re
import warnings


 
class StockMoveInherit(models.Model):
    _inherit = 'product.sample'

    def post_inventory(self):
        res = True
        acc_inventories = self.filtered(lambda inventory: inventory.accounting_date)
        for inventory in acc_inventories:
            res = super(StockMoveInherit, inventory.with_context(force_period_date=inventory.accounting_date)).post_inventory()
        other_inventories = self - acc_inventories
        if other_inventories:
            res = super(StockMoveInherit, other_inventories).post_inventory()
        return res

