from odoo import api, fields, models


class TaxReportingWizard(models.TransientModel):
    _name = 'tax.reporting.wizard'
    _description = 'tax reporting wizard'

    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')

    account_move_line_ids = fields.Many2many(
        comodel_name='account.move.line',
        string='Accounts')

    line_ids = fields.One2many(
        comodel_name='tax.reporting.line.wizard',
        inverse_name='wizard_id',
        string='Tax.reporting.line.wizard',
        required=False)

    def action_create_tax_report(self):
        domain = [('account_id.code', 'in', ('132000', '252001'))]
        if self.start_date:
            domain.append(('date', '>=', self.start_date))
        if self.end_date:
            domain.append(('date', '<=', self.end_date))

        records = self.env['account.move.line'].search(domain)
        result = {}
        for rec in records:
            if result.get(rec.account_id.name, False):
                if rec.credit:
                    amount = rec.credit
                else:
                    amount = rec.debit * (-1)
                result[rec.account_id.name] += amount
            else:
                if rec.credit:
                    amount = rec.credit
                else:
                    amount = rec.debit * (-1)
                result[rec.account_id.name] = amount
        print(result)

        for key, value in result.items():
            self.write({'line_ids': [(0, 0, {
                'name': key,
                'amount': value
            })]})
        # print('test', len(self.account_move_line_ids))
        return self.env.ref('hh_sales_inherit.taxes_wizard_report').report_action(self)


class TaxReportingWizardLine(models.TransientModel):
    _name = 'tax.reporting.line.wizard'
    _description = 'tax reporting line wizard'

    wizard_id = fields.Many2one(
        comodel_name='tax.reporting.wizard',
        string='Wizard_id',
        required=False)

    name = fields.Char(
        string='Name',
        required=False)

    amount = fields.Float(
        string='Amount',
        required=False)
