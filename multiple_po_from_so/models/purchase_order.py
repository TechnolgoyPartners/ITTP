from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    sale_order_id = fields.Many2one(comodel_name="sale.order", string="Sale", required=False, )
    sale_customer_id = fields.Many2one(comodel_name="res.partner", string="Customer",
                                       related='sale_order_id.partner_id')
