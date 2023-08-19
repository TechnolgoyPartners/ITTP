from odoo import api, fields, models, _

from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools import float_is_zero, float_compare


class Product(models.Model):
    _inherit = 'product.template'

    barcode = fields.Char(string="Product Number", )


class ProductProduct(models.Model):
    _inherit = 'product.product'

    barcode = fields.Char(string="Product Number", )

    _sql_constraints = [
        ('barcode_uniq', 'check(1=1)', ""),
    ]
