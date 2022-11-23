from odoo import fields,models,api,tools
from datetime import datetime,date,timedelta



class Menu(models.Model):
    _inherit = 'ir.ui.menu'
    

    @tools.ormcache('frozenset(self.env.user.groups_id.ids)', 'debug')
    def _visible_menu_ids(self, debug=False):
        
        menus = super(Menu,self)._visible_menu_ids(debug)
        login = self.env.user.has_group('account.group_account_user')
        print(login,'testLogin')

        if login == False:
            menus.discard(self.env.ref("account.menu_finance").id)

        return menus
