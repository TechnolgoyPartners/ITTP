from odoo import models, fields, api
from odoo.osv import expression
from datetime import datetime


class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'

    @api.onchange('line_ids')
    def onchange_line_ids(self):
        if self.line_ids:
            self.balance_end_real = self.balance_end
