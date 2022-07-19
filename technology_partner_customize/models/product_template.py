from odoo import api, fields, models, _

from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools import float_is_zero, float_compare


class Product(models.Model):
    _inherit = 'product.template'

    # type = fields.Selection(default='service')
    # detailed_type = fields.Selection(default='service')
    #
    # service_to_purchase = fields.Boolean(default=True)

    barcode = fields.Char(string="Product Number", )


class ProductProduct(models.Model):
    _inherit = 'product.product'

    barcode = fields.Char(string="Product Number", )
