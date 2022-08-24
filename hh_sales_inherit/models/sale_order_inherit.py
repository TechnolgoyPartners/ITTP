from odoo import api, fields, models


class SaleOrderInheritCustom(models.Model):
    _inherit = 'sale.order'

    shipping_term_custom_id = fields.Many2one(
        comodel_name='shipping.term.custom',
        string='Shipping Term',
        required=False)

    shipping_note = fields.Text(
       string="Shipping Note",
       required=False,
       related='shipping_term_custom_id.shipping_note')

    quotation_template_custom_id = fields.Many2one(
        comodel_name='quotation.template.custom',
        string='Quotation Template',
        required=False)

    note = fields.Text(
        string="Note",
        required=False,
        related='quotation_template_custom_id.note')


