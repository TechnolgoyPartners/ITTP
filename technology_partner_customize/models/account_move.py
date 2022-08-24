from odoo import api, fields, models, _

from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools import float_is_zero, float_compare


class AccountMove(models.Model):
    _inherit = 'account.move'

    sale_reference = fields.Char(string="Customer Reference", )


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    serial_number = fields.Char(string="Serial Number", required=False, )
    product_serial = fields.Char(string="Product Serial", related='product_id.barcode', )

    purchase_cost = fields.Float(string="Purchase Cost", required=False, )
