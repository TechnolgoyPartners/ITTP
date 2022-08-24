from odoo import api, fields, models


class ShippingTermCustom(models.Model):
    _name = 'shipping.term.custom'
    _description = 'Shipping Term Custom'

    name = fields.Char(required=True, translate=True)

    shipping_note = fields.Text(
        string="Shipping Note",
        required=True)

