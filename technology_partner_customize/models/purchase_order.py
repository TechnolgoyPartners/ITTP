from odoo import api, fields, models, _

from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools import float_is_zero, float_compare


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    serial_number = fields.Char(string="Serial Number", required=False, )
    product_serial = fields.Char(string="Product Number")

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
    
    @api.onchange("product_id")
    def _onchange_product_id(self):
        if self.product_id:
            self.product_serial = self.product_id.barcode
        else:
            self.product_serial = self.product_serial

    @api.onchange("product_serial")
    def _onchange_product_serial(self):
        current_product = self.env['product.product'].search([('barcode', '=', self.product_serial)])
        if self.product_serial:
            self.product_id = current_product.id
        else:
            self.product_id = self.product_id
