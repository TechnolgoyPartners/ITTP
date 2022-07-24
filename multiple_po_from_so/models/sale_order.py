from odoo import models, fields, api
from datetime import datetime


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_purchase_created = fields.Boolean(string="Purchase Created", copy=False)

    purchase_count = fields.Integer('Purchase', compute='_compute_purchase_count')

    def _compute_purchase_count(self):
        for rec in self:
            rec.purchase_count = self.env['purchase.order'].search_count([('sale_order_id', '=', rec.id)])

    def action_purchase_order(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Request for Quotation',
            'res_model': 'purchase.order',
            'view_mode': 'tree,form',
            'domain': [('sale_order_id', '=', self.id)],
        }

    def action_create_rfq(self):
        purchase_order_obj = self.env['purchase.order']
        purchase_order_line_obj = self.env['purchase.order.line']
        for rec in self.order_line:
            for vendor in rec.partner_ids:
                pur_order = purchase_order_obj.search(
                    [('sale_order_id', '=', self.id), ('partner_id', '=', vendor.id)])
                if pur_order:
                    po_line_vals = {
                        'product_id': rec.product_id.id,
                        'product_qty': rec.product_uom_qty,
                        'name': rec.name,
                        'price_unit': rec.product_id.standard_price,
                        'date_planned': datetime.now(),
                        'product_uom': rec.product_uom.id,
                        'order_id': pur_order.id,
                    }
                    purchase_order_line_obj.create(po_line_vals)
                else:
                    vals = {
                        'partner_id': vendor.id,
                        'date_order': datetime.now(),
                        'sale_order_id': self.id
                    }
                    purchase_order = purchase_order_obj.create(vals)
                    po_line_vals = {
                        'product_id': rec.product_id.id,
                        'product_qty': rec.product_uom_qty,
                        'name': rec.name,
                        'price_unit': rec.product_id.standard_price,
                        'date_planned': datetime.now(),
                        'product_uom': rec.product_uom.id,
                        'order_id': purchase_order.id,
                    }
                    purchase_order_line_obj.create(po_line_vals)
        self.is_purchase_created = True

    def action_multiquotation(self):
        if self.is_multiquotation:
            self.is_multiquotation = False
        else:
            self.create_automatic_muliquotation()
            self.is_multiquotation = True

    def create_automatic_muliquotation(self):
        self.multi_order_lines.unlink()
        quotation_obj = self.env['multi.quotations']
        purchase_records = self.env['purchase.order'].search([('sale_order_id', '=', self.id)])
        for purchase_record in purchase_records:
            multi_quotations = []
            for rec in purchase_record.order_line:
                multi_quotations.append((0, 0, {
                    'order_id': self.id,
                    'product_id': rec.product_id.id,
                    'name': rec.name,
                    'product_uom': rec.product_uom.id,
                    'product_uom_qty': rec.product_uom_qty,
                    'price_unit': rec.price_unit,
                    'tax_id': rec.taxes_id.ids,
                }))
            quotation_obj.create({
                'multi_order_id': self.id,
                'partner_id': self.partner_id.id,
                'pricelist_id': self.pricelist_id.id,
                'multi_quotation_line': multi_quotations,
            })


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    partner_ids = fields.Many2many(comodel_name="res.partner", string="Vendors", compute='_compute_partner_ids',
                                   readonly=False, store=True)

    @api.depends('product_id')
    def _compute_partner_ids(self):
        for rec in self:
            if rec.product_id.seller_ids:
                rec.partner_ids = rec.product_id.seller_ids.mapped('name').ids

    def _prepare_invoice_line(self, **optional_values):
        res = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
        purchase_records = self.env['purchase.order.line'].search([
            ('product_id', '=', self.product_id.id),
            ('order_id.sale_order_id', '=', self.order_id.id),
        ])
        res.update({
            'purchase_cost': sum(purchase_records.mapped('price_unit')),
        })
        return res
