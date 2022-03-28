# ©  2008-2021 Deltatech
# See README.rst file on addons root folder for license details


from odoo import fields, models, _
from odoo.exceptions import UserError


class CommissionUserInvoice(models.Model):
    _name = "commission.users.invoice"
    _rec_name = "user_id"
    _description = "Users commission Invoice"

    user_id = fields.Many2one("res.users", string="Salesperson", required=True)

    total_commission = fields.Float(string="Commission", required=False, )

    invoice_ids = fields.Many2many(comodel_name="account.move", string="Invoices", )

    date = fields.Date(string="Date", default=fields.Date.context_today)

    state = fields.Selection(string="Status", selection=[('new', 'New'), ('done', 'Done'), ], default='new', )

    def search_user_commission(self):
        target = self.env['commission.users'].search([('user_id', '=', self.user_id.id)], limit=1).target
        records = self.env['sale.margin.report'].search([
            ('user_id', '=', self.user_id.id),
            ('invoice_id.is_comm_created', '=', False)
        ])
        if records:
            self.invoice_ids = records.mapped('invoice_id').ids
            total_sales = sum(records.mapped('profit_val'))
            if total_sales > target:
                self.total_commission = sum(records.mapped('commission_computed'))
        return records

    def action_done(self):
        for rec in self.invoice_ids:
            rec.is_comm_created = True
        self.state = 'done'

    def unlink(self):
        if self.filtered(lambda rec: rec.state == 'done'):
            raise UserError(_("You cannot delete Done Records."))
        return super(CommissionUserInvoice, self).unlink()
