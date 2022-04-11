from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class UserCommission(models.Model):
    _name = 'user.commission'
    _rec_name = 'name'
    _description = 'User Commission Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Basic
    name = fields.Char(string="Name", required=True, copy=False)
    active = fields.Boolean(string="Active", default=True)
    date = fields.Date(string="Date", required=False, default=fields.Date.context_today, tracking=True)

    description = fields.Char(string="Description", required=False, )

    line_ids = fields.One2many(comodel_name="user.commission.line", inverse_name="commission_id", string="Lines",
                               required=False, )


class UserCommissionLine(models.Model):
    _name = 'user.commission.line'
    _rec_name = 'name'
    _description = 'User Commission Management Line'
    _order = 'name'

    name = fields.Integer(string="Seq", required=False, )
    commission_id = fields.Many2one(comodel_name="user.commission", string="Commission", required=False, )

    start_amount = fields.Float(string="From", required=False, )
    end_amount = fields.Float(string="To", required=False, )
    commission = fields.Float(string="Commission", required=False, )

    @api.constrains('start_amount', 'end_amount')
    def _check_start_end_amount(self):
        for rec in self:
            if rec.start_amount > rec.end_amount:
                raise ValidationError(_('Please add Valid Amount.'))
