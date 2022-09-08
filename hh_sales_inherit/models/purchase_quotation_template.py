from odoo import api, fields, models


class PurchaseQuotationTemplate(models.Model):
    _name = 'purchase.quotation.template'
    _description = 'Purchase Quotation Template'

    name = fields.Char(required=True, translate=True)

    note = fields.Text(
        string="Note",
        required=True)

