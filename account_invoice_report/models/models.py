# -*- coding: utf-8 -*-

from odoo import models, fields, api

class invoice_report(models.Model):
    _inherit = 'account.move'

    en_amount_text = fields.Char(compute='get_en_amount_text', store=True)

    @api.depends('currency_id','amount_total')
    def get_en_amount_text(self):
        for rec in self:
            rec.en_amount_text = rec.currency_id.amount_to_text(rec.amount_total)


class invoice_line_report(models.Model):
    _inherit = 'account.move.line'

    discount_amount = fields.Float(compute='calculate_discount_amount', store=True)

    @api.depends('discount','price_unit','quantity')
    def calculate_discount_amount(self):
        for rec in self:
            rec.discount_amount = ((rec.quantity * rec.price_unit) * rec.discount) / 100


