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

from odoo import models, fields, api


class MultiQuotationSelector(models.TransientModel):
    _name = 'multi.quotations.selector'

    def set_quotation(self):
        self.order_id.is_multiquotation = False
        self.order_id.order_line = False
        for line in self.best_quotation.multi_quotation_line:
            val = {
                'product_uom_qty': line.product_uom_qty,
                'order_id': self.order_id.id,
                'tax_id': [[6, False, line.tax_id.ids]],
                'product_id': line.product_id.id,
                'price_unit': line.price_unit,
                'product_uom': line.product_uom.id,
                'name': line.name,
                'discount': line.discount,
                'customer_lead': line.customer_lead,
                'analytic_tag_ids': [[6, False, line.analytic_tag_ids.ids]],
                'sequence': 10
            }
            line_cre = self.env['sale.order.line'].create(val)

    best_quotation = fields.Many2one('multi.quotations', string='Select the Quotation')
    order_id = fields.Many2one('sale.order', string='Order Reference', ondelete='cascade', index=True,
                               copy=False)
