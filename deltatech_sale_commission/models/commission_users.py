# ©  2008-2021 Deltatech
# See README.rst file on addons root folder for license details


from odoo import fields, models, api, _
from datetime import datetime
import calendar


def last_month_day(today):
    return calendar.monthrange(today.year, today.month)[1]


class CommissionUsers(models.Model):
    _name = "commission.users"
    _description = "Users commission"

    user_id = fields.Many2one("res.users", string="Salesperson", required=True)
    name = fields.Char(string="Name", related="user_id.name")
    rate = fields.Float(string="Rate", compute='_compute_commission_rate', store=True)
    manager_rate = fields.Float(string="Rate manager", default=0, digits=(12, 3))
    manager_user_id = fields.Many2one("res.users", string="Sales Manager")
    journal_id = fields.Many2one("account.journal", string="Journal", domain="[('type', 'in', ['sale','sale_refund'])]")

    commission_id = fields.Many2one(comodel_name="user.commission", string="Commission", required=False, )

    @api.depends('commission_id')
    def _compute_commission_rate(self):
        for rec in self:
            if rec.commission_id:
                rec.rate = 0.0
                domain = [
                    ('user_id', '=', self.user_id.id),
                    # ('date', '>=', datetime.now().date().replace(day=1)),
                    # ('date', '<=', datetime.now().date().replace(day=last_month_day(datetime.now()))),
                ]
                records = self.env['sale.margin.report'].search(domain)
                total_sales = sum(records.mapped('profit_val'))
                for line in rec.commission_id.line_ids:
                    if line.start_amount <= total_sales < line.end_amount:
                        rec.rate = line.commission
                        break
            else:
                rec.rate = 0.0
