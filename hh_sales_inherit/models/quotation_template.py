from odoo import api, fields, models


class QuotationTemplateCustom(models.Model):
    _name = 'quotation.template.custom'
    _description = 'Quotation Template Custom'

    name = fields.Char(required=True, translate=True)

    note = fields.Text(
        string="Note",
        required=True)

