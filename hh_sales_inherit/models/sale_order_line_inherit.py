from odoo import api, fields, models


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

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

