
import datetime
from unicodedata import category
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime,timedelta,date

class Anggaran(models.Model):
    _name = "project.anggaran"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "For Project Budget"
    _order = "id desc"
   
    id = fields.Char(string='ID')
    description = fields.Char(string='Description')
    date_plan = fields.Date(string="Tanggal Perencanaan")
    budget = fields.Monetary(string='Budget')
    total_budget = fields.Monetary(string='Total Penerimaan')
    project = fields.Many2one('project.project',string="Project")

    