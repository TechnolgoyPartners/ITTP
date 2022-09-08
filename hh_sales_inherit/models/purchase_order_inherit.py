from odoo import api, fields, models


class PurchaseOrderInheritCustom(models.Model):
    _inherit = 'purchase.order'
    
    purchase_order_seq = fields.Char(
        string='Purchase Seq',
        required=False)

    shipping_term_custom_id = fields.Many2one(
        comodel_name='purchase.shipping.term',
        string='Shipping Term',
        required=False)

    shipping_note = fields.Text(
        string="Shipping Note",
        required=False,
        related='shipping_term_custom_id.shipping_note')

    quotation_template_custom_id = fields.Many2one(
        comodel_name='purchase.quotation.template',
        string='Quotation Template',
        required=False)

    note = fields.Text(
        string="Note",
        required=False,
        related='quotation_template_custom_id.note')

    def button_confirm(self):
        res = super(PurchaseOrderInheritCustom, self).button_confirm()
        print('hello from confirm order button')
        self.purchase_order_seq = self.env['ir.sequence'].next_by_code('purchase.order.custom')
        return res
