from odoo import api, fields, models


class PurchaseOrderInherit(models.Model):
    _inherit = ['purchase.order']

    def print_reciept(self):
        return self.env.ref('stock.action_report_picking').report_action(self.picking_ids)
        # context = dict(self.env.context, active_ids=self.picking_ids.ids)
        #
        # report_action = {
        #     'id': 'action_report_picking',
        #     'context': context,
        #     'model': 'stock.picking',
        #     'type': 'ir.actions.report',
        #     'report_name': 'stock.report_picking',
        #     'report_type': 'qweb-pdf',
        #     'report_file': 'stock.report_picking_operations',
        #     'name': "Picking Operations",
        # }
        # return report_action

