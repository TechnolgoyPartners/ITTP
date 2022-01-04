# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from odoo import models, fields, api

class TccResCurrency(models.Model):
    _inherit = 'res.currency'

    def amount_to_text(self, amount):
        self.ensure_one()
        def _num2words(number, lang):
            try:
                return num2words(number, lang=lang).title()
            except NotImplementedError:
                return num2words(number, lang='en').title()
        if num2words is None:
            logging.getLogger(__name__).warning("The library 'num2words' is missing, cannot render textual amounts.")
            return ""
        formatted = "%.{0}f".format(self.decimal_places) % amount
        parts = formatted.partition('.')
        integer_value = int(parts[0])
        fractional_value = int(parts[2] or 0)
        lang_code = self.env.context.get('lang') or self.env.user.lang
        lang = self.env['res.lang'].with_context(active_test=False).search([('code', '=', lang_code)])
        if lang_code == 'ar_AA':
            amount_words = tools.ustr('{amt_value} {amt_word}').format(
                amt_value=_num2words(integer_value, lang=lang.iso_code),
                amt_word='ريال',
            )
            if not self.is_zero(amount - integer_value):
                amount_words += ' ' + _('and') + tools.ustr(' {amt_value} {amt_word}').format(
                    amt_value=_num2words(fractional_value, lang=lang.iso_code),
                    amt_word='هللة',
                )
        else:
            amount_words = tools.ustr('{amt_value} {amt_word}').format(
                amt_value=_num2words(integer_value, lang=lang.iso_code),
                amt_word=self.currency_unit_label,
            )
            if not self.is_zero(amount - integer_value):
                amount_words += ' ' + _('and') + tools.ustr(' {amt_value} {amt_word}').format(
                    amt_value=_num2words(fractional_value, lang=lang.iso_code),
                    amt_word=self.currency_subunit_label,
                )
        return amount_words

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




