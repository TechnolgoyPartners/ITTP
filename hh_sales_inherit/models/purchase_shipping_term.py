from odoo import api, fields, models


class PurchaseShippingTerm(models.Model):
    _name = 'purchase.shipping.term'
    _description = 'Purchase Shipping Term'

    name = fields.Char(required=True, translate=True)

    shipping_note = fields.Text(
        string="Shipping Note",
        required=True)

