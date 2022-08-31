from odoo import api, fields, models


class PurchaseOrderInheritCustom(models.Model):
    _inherit = 'purchase.order'
    
    purchase_order_seq = fields.Char(
        string='Purchase Seq', compute='_compute_purchase_order_seq',
        required=False)

    @api.depends('state')
    def _compute_purchase_order_seq(self):
        if self.state == 'purchase':
            self.purchase_order_seq = self.env['ir.sequence'].next_by_code('purchase.order.custom')
        else:
            self.purchase_order_seq = 0
