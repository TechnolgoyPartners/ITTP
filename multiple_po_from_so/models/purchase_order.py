from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    sale_order_id = fields.Many2one(comodel_name="sale.order", string="Sale", required=False, readonly=False)
    sale_customer_id = fields.Many2one(comodel_name="res.partner", string="Customer",
                                       related='sale_order_id.partner_id')

    is_customer = fields.Boolean(
        string='Is Customer',
        required=False, default=False)

