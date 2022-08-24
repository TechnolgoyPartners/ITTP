# -*- coding: utf-8 -*-

import logging
import math
import re
import time
import num2word
from lxml import etree
from odoo import api, fields, models, tools, _

_logger = logging.getLogger(__name__)

try:
    from num2words import num2words
except ImportError:
    _logger.warning("The num2words python library is not installed, amount-to-text features won't be fully available.")
    num2words = None

CURRENCY_DISPLAY_PATTERN = re.compile(r'(\w+)\s*(?:\((.*)\))?')


class Currency(models.Model):
    _inherit = 'res.currency'

    decimal_places = fields.Integer(compute='_compute_decimal_places', store=True,
                                    help='Decimal places taken into account for operations on amounts in this currency. It is determined by the rounding factor.')
    currency_unit_label = fields.Char(string="Currency Unit", help="Currency Unit Name")
    currency_subunit_label = fields.Char(string="Currency Subunit", help="Currency Subunit Name")
    ar_currency_unit_label = fields.Char(string="Currency Unit AR", help="Currency Unit Name")
    ar_currency_subunit_label = fields.Char(string="Currency Subunit AR", help="Currency Subunit Name")
    rounding = fields.Float(string='Rounding Factor', digits=(12, 6), default=0.01,
                            help='Amounts in this currency are rounded off to the nearest multiple of the rounding factor.')

    def amount_to_text_ar(self, amount):
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

        lang = tools.get_lang(self.env)
        amount_words = tools.ustr('{amt_value} {amt_word}').format(
                        amt_value=_num2words(integer_value, lang='ar_001'),
                        amt_word=self.ar_currency_unit_label,
                        )
        if not self.is_zero(amount - integer_value):
            amount_words += ' ' +  tools.ustr(' {amt_value} {amt_word}').format(
                        amt_value=_num2words(fractional_value, lang='ar_001'),
                        amt_word=self.ar_currency_subunit_label,
                        )
        return amount_words

    def amount_to_text_en(self, amount):
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

        lang = tools.get_lang(self.env)
        amount_words = tools.ustr('{amt_value} {amt_word}').format(
                        amt_value=_num2words(integer_value, lang='en_US'),
                        amt_word=self.currency_unit_label,
                        )
        if not self.is_zero(amount - integer_value):
            amount_words += ' ' + _('and') + tools.ustr(' {amt_value} {amt_word}').format(
                        amt_value=_num2words(fractional_value, lang='en_US'),
                        amt_word=self.currency_subunit_label,
                        )
        return amount_words

    def is_zero(self, amount):
        """Returns true if ``amount`` is small enough to be treated as
           zero according to current currency's rounding rules.
           Warning: ``is_zero(amount1-amount2)`` is not always equivalent to
           ``compare_amounts(amount1,amount2) == 0``, as the former will round after
           computing the difference, while the latter will round before, giving
           different results for e.g. 0.006 and 0.002 at 2 digits precision.

           :param float amount: amount to compare with currency's zero

           With the new API, call it like: ``currency.is_zero(amount)``.
        """
        self.ensure_one()
        return tools.float_is_zero(amount, precision_rounding=self.rounding)


class invoice_report(models.Model):
    _inherit = 'account.move'

    en_amount_text = fields.Char(compute='get_en_amount_text', store=True)

    note = fields.Text(
        string="Note",
        required=False)

    is_first_print = fields.Boolean(
        string='Is_first_print',
        required=False, default=True)

    def action_print_invoice_inherited(self):
        print('hi from invoices')
        self.is_first_print = False
        return self.env.ref('account.account_invoices').report_action(self)

    @api.depends('currency_id','amount_total')
    def get_en_amount_text(self):
        for rec in self:
            rec.en_amount_text = rec.currency_id.amount_to_text_en(rec.amount_total)


    ar_amount_text = fields.Char(compute='get_ar_amount_text', store=True)

    @api.depends('amount_total')
    def get_ar_amount_text(self):
        for rec in self:
            rec.ar_amount_text = rec.currency_id.amount_to_text_ar(rec.amount_total)


class invoice_line_report(models.Model):
    _inherit = 'account.move.line'

    discount_amount = fields.Float(compute='calculate_discount_amount', store=True)

    @api.depends('discount','price_unit','quantity')
    def calculate_discount_amount(self):
        for rec in self:
            rec.discount_amount = ((rec.quantity * rec.price_unit) * rec.discount) / 100


