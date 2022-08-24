from odoo import api, fields, models, _

from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools import float_is_zero, float_compare


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    serial_number = fields.Char(string="Serial Number", required=False, )
    product_serial = fields.Char(string="Product Number", related='product_id.barcode', )

    description = fields.Char(
        string='Description',
        readonly=False)

    seq = fields.Integer(
        string='Seq', default=0,
        compute='_compute_seq_number',
        required=False)

    # @api.depends('product_id')
    def _compute_seq_number(self):
        start = 1
        for rec in self:
            rec.seq = start
            start += 1


    def _prepare_account_move_line(self, move=False):
        res = super(PurchaseOrderLine, self)._prepare_account_move_line(move)
        res.update({
            'serial_number': self.serial_number
        })
        return res
