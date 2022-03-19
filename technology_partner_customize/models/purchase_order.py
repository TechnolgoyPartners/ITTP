from odoo import api, fields, models, _

from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools import float_is_zero, float_compare


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    serial_number = fields.Char(string="Serial Number", required=False, )

    def _prepare_account_move_line(self, move=False):
        res = super(PurchaseOrderLine, self)._prepare_account_move_line(move)
        res.update({
            'serial_number': self.serial_number
        })
        return res
