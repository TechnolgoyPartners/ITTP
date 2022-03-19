from odoo import api, fields, models, _

from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools import float_is_zero, float_compare


# class SaleOrder(models.Model):
#     _inherit = 'sale.order'


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    partner_id = fields.Many2one(comodel_name="res.partner", string="Vendor", required=False, )
    serial_number = fields.Char(string="Serial Number", required=False, )

    def _purchase_service_create(self, quantity=False):
        """ On Sales Order confirmation, some lines (services ones) can create a purchase order line and maybe a purchase order.
            If a line should create a RFQ, it will check for existing PO. If no one is find, the SO line will create one, then adds
            a new PO line. The created purchase order line will be linked to the SO line.
            :param quantity: the quantity to force on the PO line, expressed in SO line UoM
        """
        PurchaseOrder = self.env['purchase.order']
        supplier_po_map = {}
        sale_line_purchase_map = {}
        for line in self:
            line = line.with_company(line.company_id)
            # determine vendor of the order (take the first matching company and product)
            if line.partner_id:
                suppliers = line.product_id._select_seller(partner_id=line.partner_id, quantity=line.product_uom_qty,
                                                           uom_id=line.product_uom)
            else:
                suppliers = line.product_id._select_seller(quantity=line.product_uom_qty,
                                                           uom_id=line.product_uom)
            if not suppliers:
                raise UserError(
                    _("There is no vendor associated to the product %s. Please define a vendor for this product.") % (
                        line.product_id.display_name,))
            supplierinfo = suppliers[0]
            partner_supplier = supplierinfo.name  # yes, this field is not explicit .... it is a res.partner !

            # determine (or create) PO
            purchase_order = supplier_po_map.get(partner_supplier.id)
            if not purchase_order:
                purchase_order = PurchaseOrder.search([
                    ('partner_id', '=', partner_supplier.id),
                    ('state', '=', 'draft'),
                    ('company_id', '=', line.company_id.id),
                ], limit=1)
            if not purchase_order:
                values = line._purchase_service_prepare_order_values(supplierinfo)
                purchase_order = PurchaseOrder.create(values)
            else:  # update origin of existing PO
                so_name = line.order_id.name
                origins = []
                if purchase_order.origin:
                    origins = purchase_order.origin.split(', ') + origins
                if so_name not in origins:
                    origins += [so_name]
                    purchase_order.write({
                        'origin': ', '.join(origins)
                    })
            supplier_po_map[partner_supplier.id] = purchase_order

            # add a PO line to the PO
            values = line._purchase_service_prepare_line_values(purchase_order, quantity=quantity)
            values['serial_number'] = line.serial_number
            purchase_line = line.env['purchase.order.line'].create(values)

            # link the generated purchase to the SO line
            sale_line_purchase_map.setdefault(line, line.env['purchase.order.line'])
            sale_line_purchase_map[line] |= purchase_line
        return sale_line_purchase_map

    def _prepare_invoice_line(self, **optional_values):
        res = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
        res.update({
            'serial_number': self.serial_number
        })
        return res
