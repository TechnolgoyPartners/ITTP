# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2018-TODAY NIKHIL KRISHNAN(nikhilkrishnan0101@gmail.com).
#    Author: Nikhil krishnan(nikhilkrishnan0101@gmail.com)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from itertools import groupby
from odoo import models, fields, api, _


class MultiQuotations(models.Model):
    _name = 'multi.quotations'

    @api.model
    def default_get(self, default_fields):
        res = super(MultiQuotations, self).default_get(default_fields)
        sale_id = self.env.context.get('default_multi_order_id', [])
        record = self.env['sale.order'].browse(sale_id)
        update = []
        for rec in record.order_line:
            update.append((0, 0, {
                'order_id': sale_id,
                'product_id': rec.product_id.id,
                'name': rec.name,
                'product_uom': rec.product_uom.id,
                'product_uom_qty': rec.product_uom_qty,
                'price_unit': rec.price_unit,
                'tax_id': rec.tax_id,
            }))
        res.update({'multi_quotation_line': update})
        return res

    @api.depends('multi_quotation_line.price_total')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.multi_quotation_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            order.update({
                'amount_untaxed': order.pricelist_id.currency_id.round(amount_untaxed),
                'amount_tax': order.pricelist_id.currency_id.round(amount_tax),
                'amount_total': amount_untaxed + amount_tax,
            })

    @api.model
    def _default_note(self):
        return self.env['ir.config_parameter'].sudo().get_param(
            'sale.use_sale_note') and self.env.user.company_id.sale_note or ''

    name = fields.Char(string='Quotation Number')
    multi_order_id = fields.Many2one('sale.order', string='Order Reference', ondelete='cascade', index=True,
                                     copy=False)
    partner_id = fields.Many2one('res.partner', string='Customer')
    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist', required=True,
                                   help="Pricelist for current sales order.")
    company_id = fields.Many2one('res.company', string='Company', change_default=True,
                                 default=lambda self: self.env['res.company']._company_default_get(
                                     'ir.attachment'))
    product_count = fields.Integer(string='Number of Products')
    multi_quotation_line = fields.One2many('multi.quotation.line', 'multi_quotation_id', string='Order Lines',
                                           copy=True, auto_join=True)
    currency_id = fields.Many2one("res.currency", related='pricelist_id.currency_id', string="Currency", readonly=True,
                                  required=True)
    amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all',
                                     track_visibility='onchange')
    amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_all')
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all',
                                   track_visibility='always')
    note = fields.Text('Terms and conditions', default=_default_note)
    tax_country_id = fields.Many2one(related="multi_order_id.tax_country_id", store=True)
    state = fields.Selection(related="multi_order_id.state", store=True)

    def write(self, values):
        i = 0
        if values.get('multi_quotation_line'):
            for line in values['multi_quotation_line']:
                i = i + 1
        else:
            i = 0
        values['product_count'] = i
        return super(MultiQuotations, self).write(values)

    @api.model
    def create(self, values):
        # values.update(self._prepare_add_missing_fields(values))
        sale_order_id = self.env['sale.order'].search([('id', '=', values['multi_order_id'])])
        new_name = sale_order_id.name + self.env['ir.sequence'].next_by_code('multi.quotation')
        values['name'] = new_name
        i = 0
        if values.get('multi_quotation_line'):
            for line in values['multi_quotation_line']:
                i = i + 1
        values['product_count'] = i

        if any(f not in values for f in ['partner_invoice_id', 'partner_shipping_id', 'pricelist_id']):
            partner = self.env['res.partner'].browse(values.get('partner_id'))
            values['pricelist_id'] = values.setdefault('pricelist_id',
                                                       partner.property_product_pricelist and partner.property_product_pricelist.id)
        return super(MultiQuotations, self).create(values)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_multi_quotation_selector(self):
        ctx = {
            'default_model': 'sale.order',
            'default_order_id': self.id,
        }

        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'multi.quotations.selector',
            'view_id': self.env.ref('multiple_quotation_handler.view_multi_quotation_selector').id,
            'target': 'new',
            'context': ctx,
        }

    def _get_multi_tax_amount_by_group(self, val):
        self.ensure_one()
        res = {}
        for line in val.multi_quotation_line:
            price_reduce = line.price_unit * (1.0 - line.discount / 100.0)
            taxes = line.tax_id.compute_all(price_reduce, quantity=line.product_uom_qty, product=line.product_id,
                                            partner=self.partner_shipping_id)['taxes']
            for tax in line.tax_id:
                group = tax.tax_group_id
                res.setdefault(group, {'amount': 0.0, 'base': 0.0})
                for t in taxes:
                    if t['id'] == tax.id or t['id'] in tax.children_tax_ids.ids:
                        res[group]['amount'] += t['amount']
                        res[group]['base'] += t['base']
        res = sorted(res.items(), key=lambda l: l[0].sequence)
        res = [(l[0].name, l[1]['amount'], l[1]['base'], len(res)) for l in res]
        return res

    def order_lines_multi_layouted(self, val):
        """
        Returns this order lines classified by sale_layout_category and separated in
        pages according to the category pagebreaks. Used to render the report.
        """
        self.ensure_one()
        report_pages = [[]]
        for category, lines in groupby(val.multi_quotation_line):
            # If last added category induced a pagebreak, this one will be on a new page
            if report_pages[-1] and report_pages[-1][-1]['pagebreak']:
                report_pages.append([])
            # Append category to current report page
            report_pages[-1].append({
                'name': category and category.name or _('Uncategorized'),
                'price_subtotal': category and category.price_subtotal,
                'pagebreak': True,
                'lines': list(lines)
            })

        return report_pages

    def order_lines_multiple_layouted(self):
        """
        Returns this multiple Quotation lines. Used to render the report.
        """
        self.ensure_one()
        report_pages = []
        for multi_order_line in self.multi_order_lines:
            report_pages.append(multi_order_line)
        return report_pages

    def action_multiquotation(self):
        if self.is_multiquotation:
            self.is_multiquotation = False
        else:
            self.is_multiquotation = True

    def _find_mail_template(self, force_confirmation_template=False):
        template_id = super(SaleOrder, self)._find_mail_template(force_confirmation_template)
        if self.is_multiquotation:
            template_id = self.env['ir.model.data']._xmlid_to_res_id(
                'multiple_quotation_handler.email_template_multi_quotation',
                raise_if_not_found=False)
        return template_id

    is_multiquotation = fields.Boolean(string='Enable multi-Quotation', readonly=True, copy=False)
    multiquotation_note = fields.Text(string='Quotation Note', help="Report footer Note",
                                      default='Decision is yours, choose the best.', copy=False)
    multi_order_lines = fields.One2many('multi.quotations', 'multi_order_id', string='Order Lines', copy=False)


class MultiQuotationOrderLine(models.Model):
    _name = 'multi.quotation.line'
    _inherit = ['sale.order.line']

    @api.model
    def _default_order_id(self):
        return self.env.context.get('default_order_id', [])

    multi_quotation_id = fields.Many2one('multi.quotations', string='Order Reference', copy=False)
    order_id = fields.Many2one('sale.order', string='Order Reference', ondelete='cascade', index=True,
                               copy=False, default=_default_order_id)

    invoice_lines = fields.Many2many('account.move.line', 'multi_quotation_line_invoice_rel', 'quotation_line_id',
                                     'invoice_line_id', string='Invoice Lines', copy=False)
