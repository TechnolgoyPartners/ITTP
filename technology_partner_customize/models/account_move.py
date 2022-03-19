from odoo import api, fields, models, _

from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools import float_is_zero, float_compare


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    serial_number = fields.Char(string="Serial Number", required=False, )
