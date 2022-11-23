
from datetime import datetime,timedelta
from shutil import move
from odoo import models, fields, api,_
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_is_zero

class ProductCategory(models.Model):
    _inherit = "product.category"

    property_account_output_production_categ_id = fields.Many2one(
        'account.account', 'Manufactur Output Account', company_dependent=True,
        domain="[('company_id', '=', allowed_company_ids[0]), ('deprecated', '=', False)]", check_company=True,
        help="""When doing automated inventory valuation, counterpart journal items for all outgoing stock moves will be posted in this account,
                unless there is a specific valuation account set on the destination location. This is the default value for all products in this category.
                It can also directly be set on each product.""")
    property_account_input_production_categ_id = fields.Many2one(
        'account.account', 'Manufactur Input Account', company_dependent=True,
        domain="[('company_id', '=', allowed_company_ids[0]), ('deprecated', '=', False)]", check_company=True,
        help="""When doing automated inventory valuation, counterpart journal items for all outgoing stock moves will be posted in this account,
                unless there is a specific valuation account set on the destination location. This is the default value for all products in this category.
                It can also directly be set on each product.""")