from odoo import api, fields, models

import time
import base64
import xlsxwriter
import io


class PartnerAccountReportWizard(models.TransientModel):
    _name = 'partner.account.report.wizard'
    _description = 'Partner Account Report Wizard'

    start_date = fields.Date('Start Date', default=time.strftime('%Y-01-01'))
    end_date = fields.Date('End Date', default=fields.Date.context_today)

    currency_id = fields.Many2one(
        'res.currency',
        default=lambda self: self.env.user.company_id.currency_id,
        string='Currency',
    )

    partner_ids = fields.Many2many(
        comodel_name='res.partner',
        string="Filter Partner")

    account_ids = fields.Many2many(
        comodel_name='account.account',
        string='Filter Accounts')

    journal_ids = fields.Many2many(
        comodel_name='account.journal',
        string='Filter Journals')

    account_analytic_ids = fields.Many2many(
        comodel_name='account.analytic.account',
        string='Filter Account Analytic')

    analytic_tag_ids = fields.Many2many(
        comodel_name='account.analytic.tag',
        string='Analytic Tags')

    move_state = fields.Selection(string="Move Status", selection=[('posted', 'Posted'), ('all', 'All'), ],
                                  default='all', )

    account_move_line_ids = fields.Many2many(
        comodel_name='account.move.line',
        string='Account Lines')

    is_initial_balance = fields.Boolean(string="Initial Balance", default=True)

    excel_sheet = fields.Binary()

    def get_initial_balance(self, object_id, status, account=False):
        domain = [
            ('date', '<', self.start_date),
        ]
        if status == 'partner':
            domain.extend([
                ('partner_id', '=', object_id),
                ('account_id', '=', account)
            ])
        elif status == 'journal':
            if self.account_ids:
                domain.append(('account_id', 'in', self.account_ids.ids))
            domain.append(('journal_id', '=', object_id))
        elif status == 'analytic':
            if self.account_ids:
                domain.append(('account_id', 'in', self.account_ids.ids))
            domain.append(('analytic_account_id', '=', object_id))
        elif status == 'tag':
            if self.account_ids:
                domain.append(('account_id', 'in', self.account_ids.ids))
            domain.append(('analytic_tag_ids', 'in', object_id))
        else:
            domain.append(('account_id', '=', object_id))
        records = self.env["account.move.line"].search(domain)
        if records:
            return sum(records.mapped('balance'))
        else:
            return 0.0

    def action_create_partner_report(self):
        self.account_move_line_ids = False
        domain = []
        if self.start_date:
            domain.append(('date', '>=', self.start_date))
        if self.end_date:
            domain.append(('date', '<=', self.end_date))
        if self.partner_ids:
            domain.append(('partner_id', 'in', self.partner_ids.ids))
        if self.account_ids:
            domain.append(('account_id', 'in', self.account_ids.ids))
        if self.journal_ids:
            domain.append(('journal_id', 'in', self.journal_ids.ids))
        if self.account_analytic_ids:
            domain.append(('analytic_account_id', 'in', self.account_analytic_ids.ids))
        if self.analytic_tag_ids:
            domain.append(('analytic_tag_ids', 'in', self.analytic_tag_ids.ids))
        if self.move_state == 'posted':
            domain.append(("move_id.state", "=", "posted"))
        else:
            domain.append(("move_id.state", "in", ["posted", "draft"]))
        self.account_move_line_ids = self.env['account.move.line'].search(domain)

    def print_html(self):
        self.action_create_partner_report()
        return self.env.ref('account_partner_report.partner_account_html_report').report_action(self)

    def print_pdf(self):
        self.action_create_partner_report()
        return self.env.ref('account_partner_report.partner_account_pdf_report').report_action(self)

    def get_account_name(self, account_id):
        return self.env['account.account'].browse(account_id).name

    def get_partner_name(self, partner_id):
        return self.env['res.partner'].browse(partner_id).name

    def get_journal_name(self, journal_id):
        return self.env['account.journal'].browse(journal_id).name

    def get_analytic_name(self, analytic_id):
        return self.env['account.analytic.account'].browse(analytic_id).name

    def get_analytic_tags(self):
        return self.account_move_line_ids.mapped('analytic_tag_ids')

    def get_ref_label(self, ref, label):
        if ref and label:
            return (ref + ' - ' + label).replace("\n", "")
        elif ref:
            return ref.replace("\n", "")
        elif label:
            return label.replace("\n", "")
        else:
            return ""

    def print_excel(self):
        self.action_create_partner_report()
        if self.partner_ids:
            report_name = "Partner Account Report"
        elif self.journal_ids:
            report_name = "Journal Account Report"
        elif self.account_analytic_ids:
            report_name = "Journal Account Report"
        elif self.analytic_tag_ids:
            report_name = "Analytic Tag Account Report"
        else:
            report_name = "Account Report"

        date_from = "From"
        date_to = "To"
        total = "Total"
        header_date = "Date"
        header_entry = "Entry"
        header_journal = "Journal"
        header_account = "Account"
        header_partner = "Partner"
        header_label = "Ref - Label"
        header_analytic_account = "Analytic Account"
        header_debit = "Debit"
        header_credit = "Credit"
        header_balance = "Balance"
        header_initial_balance = "Initial Balance"

        def create_header(row):
            sheet.write(row, 0, header_date, header_format)
            sheet.write(row, 1, header_entry, header_format)
            sheet.write(row, 2, header_journal, header_format)
            sheet.write(row, 3, header_account, header_format)
            sheet.write(row, 4, header_partner, header_format)
            sheet.write(row, 5, header_label, header_format)
            sheet.write(row, 6, header_analytic_account, header_format)
            sheet.write(row, 7, header_debit, header_format)
            sheet.write(row, 8, header_credit, header_format)
            sheet.write(row, 9, header_balance, header_format)

        def create_content(row, move, total_balance):
            sheet.write(row, 0, str(move.date), content_format)
            sheet.write(row, 1, move.move_id.name or '', content_format)
            sheet.write(row, 2, move.journal_id.name or '', content_format)
            sheet.write(row, 3, move.account_id.name or '', content_format)
            sheet.write(row, 4, move.partner_id.name or '', content_format)
            sheet.write(row, 5, self.get_ref_label(move.ref, move.name), content_format)
            sheet.write(row, 6, move.analytic_account_id.name or '', content_format)
            sheet.write(row, 7, move.debit, content_format)
            sheet.write(row, 8, move.credit, content_format)
            sheet.write(row, 9, round(total_balance, 2), content_format)

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)

        header_format = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'bold': 1, 'border': 2,
                                             'bg_color': '#BBDEFB'})
        content_format = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'bold': 1, 'border': 2})
        center = workbook.add_format({'align': 'center', 'valign': 'vcenter'})

        merge_format = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': '#BBDEFB'})

        merge_left_format = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'left',
            'valign': 'vcenter',
            'fg_color': '#BBDEFB'})

        merge_right_format = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'right',
            'valign': 'vcenter'})

        borders = workbook.add_format()
        borders.set_border(1)

        sheet = workbook.add_worksheet(report_name)
        sheet.conditional_format('A1:ZZ120000', {'type': 'no_errors', 'format': borders})
        sheet.set_column('A:AK', None, center)
        sheet.set_column('A:A', 15)
        sheet.set_column('B:B', 25)
        sheet.set_column('C:G', 30)
        sheet.set_column('F:F', 35)
        sheet.set_column('H:J', 15)

        sheet.merge_range('A1:D1', report_name, merge_format)
        sheet.write(1, 0, date_from, header_format)
        sheet.write(1, 1, str(self.start_date), header_format)
        sheet.write(1, 2, date_to, header_format)
        sheet.write(1, 3, str(self.end_date), header_format)

        row = 3

        if self.partner_ids:
            for account in self.account_move_line_ids.read_group(domain=[('id', 'in', self.account_move_line_ids.ids)],
                                                                 fields=['account_id'],
                                                                 groupby=['account_id'],
                                                                 orderby='account_id'):
                for partner in self.account_move_line_ids.read_group(
                        domain=[('id', 'in', self.account_move_line_ids.ids),
                                ('account_id', '=', account['account_id'][0])],
                        fields=['partner_id'],
                        groupby=['partner_id']):
                    if partner['partner_id']:
                        sheet.merge_range(row, 0, row, 9, self.get_account_name(account['account_id'][0]),
                                          merge_left_format)
                        sheet.merge_range(row + 1, 0, row + 1, 9, self.get_partner_name(partner['partner_id'][0]),
                                          merge_left_format)
                        row += 2
                        create_header(row)
                        row += 1
                        total_debit = 0
                        total_credit = 0
                        total_balance = 0
                        initial_balance = self.get_initial_balance(partner['partner_id'][0], 'partner',
                                                                   account['account_id'][0])
                        if initial_balance and self.is_initial_balance:
                            sheet.write(row, 6, header_initial_balance, content_format)
                            sheet.write(row, 9, initial_balance, content_format)
                            row += 1
                            total_balance += initial_balance
                        for move in self.account_move_line_ids.sorted(key=lambda x: x.date).filtered(
                                lambda line: line.partner_id.id == partner['partner_id'][0] and line.account_id.id ==
                                             account['account_id'][0]):
                            total_debit += move.debit
                            total_credit += move.credit
                            total_balance += (move.debit - move.credit)
                            create_content(row, move, total_balance)
                            row += 1
                        sheet.merge_range(row, 0, row, 6, total, header_format)
                        sheet.write(row, 7, total_debit, header_format)
                        sheet.write(row, 8, total_credit, header_format)
                        sheet.write(row, 9, round(total_balance, 2), header_format)
                        row += 2
        elif self.journal_ids:
            for journal in self.account_move_line_ids.read_group(
                    domain=[('id', 'in', self.account_move_line_ids.ids)],
                    fields=['journal_id'],
                    groupby=['journal_id']):
                if journal['journal_id']:
                    sheet.merge_range(row, 0, row + 1, 9, self.get_journal_name(journal['journal_id'][0]),
                                      merge_left_format)
                    row += 2
                    create_header(row)
                    row += 1
                    total_debit = 0
                    total_credit = 0
                    total_balance = 0
                    initial_balance = self.get_initial_balance(journal['journal_id'][0], 'journal')
                    if initial_balance and self.is_initial_balance:
                        sheet.write(row, 6, header_initial_balance, content_format)
                        sheet.write(row, 9, initial_balance, content_format)
                        row += 1
                        total_balance += initial_balance
                    for move in self.account_move_line_ids.sorted(key=lambda x: x.date).filtered(
                            lambda line: line.journal_id.id == journal['journal_id'][0]):
                        total_debit += move.debit
                        total_credit += move.credit
                        total_balance += (move.debit - move.credit)
                        create_content(row, move, total_balance)
                        row += 1
                    sheet.merge_range(row, 0, row, 6, total, header_format)
                    sheet.write(row, 7, total_debit, header_format)
                    sheet.write(row, 8, total_credit, header_format)
                    sheet.write(row, 9, round(total_balance, 2), header_format)
                    row += 2
        elif self.account_analytic_ids:
            for analytic in self.account_move_line_ids.read_group(
                    domain=[('id', 'in', self.account_move_line_ids.ids)],
                    fields=['analytic_account_id'],
                    groupby=['analytic_account_id']):
                if analytic['analytic_account_id']:
                    sheet.merge_range(row, 0, row + 1, 9,
                                      self.get_analytic_name(analytic['analytic_account_id'][0]),
                                      merge_left_format)
                    row += 2
                    create_header(row)
                    row += 1
                    total_debit = 0
                    total_credit = 0
                    total_balance = 0
                    initial_balance = self.get_initial_balance(analytic['analytic_account_id'][0], 'analytic')
                    if initial_balance and self.is_initial_balance:
                        sheet.write(row, 6, header_initial_balance, content_format)
                        sheet.write(row, 9, initial_balance, content_format)
                        row += 1
                        total_balance += initial_balance
                    for move in self.account_move_line_ids.sorted(key=lambda x: x.date).filtered(
                            lambda line: line.analytic_account_id.id == analytic['analytic_account_id'][0]):
                        total_debit += move.debit
                        total_credit += move.credit
                        total_balance += (move.debit - move.credit)
                        create_content(row, move, total_balance)
                        row += 1
                    sheet.merge_range(row, 0, row, 6, total, header_format)
                    sheet.write(row, 7, total_debit, header_format)
                    sheet.write(row, 8, total_credit, header_format)
                    sheet.write(row, 9, round(total_balance, 2), header_format)
                    row += 2
        elif self.analytic_tag_ids:
            tags = self.get_analytic_tags()
            for tag in tags:
                sheet.merge_range(row, 0, row + 1, 9, tag.name, merge_left_format)
                row += 2
                create_header(row)
                row += 1
                total_debit = 0
                total_credit = 0
                total_balance = 0
                initial_balance = self.get_initial_balance(tag.ids, 'tag')
                if initial_balance and self.is_initial_balance:
                    sheet.write(row, 6, header_initial_balance, content_format)
                    sheet.write(row, 9, initial_balance, content_format)
                    row += 1
                    total_balance += initial_balance
                for move in self.account_move_line_ids.sorted(key=lambda x: x.date).filtered(
                        lambda line: line.analytic_tag_ids.id == tag.id):
                    total_debit += move.debit
                    total_credit += move.credit
                    total_balance += (move.debit - move.credit)
                    create_content(row, move, total_balance)
                    row += 1
                sheet.merge_range(row, 0, row, 6, total, header_format)
                sheet.write(row, 7, total_debit, header_format)
                sheet.write(row, 8, total_credit, header_format)
                sheet.write(row, 9, round(total_balance, 2), header_format)
                row += 2
        else:
            for account in self.account_move_line_ids.read_group(domain=[('id', 'in', self.account_move_line_ids.ids)],
                                                                 fields=['account_id'],
                                                                 groupby=['account_id'],
                                                                 orderby='account_id'):
                if account['account_id']:
                    sheet.merge_range(row, 0, row, 9, self.get_account_name(account['account_id'][0]),
                                      merge_left_format)
                    row += 2
                    create_header(row)
                    row += 1
                    total_debit = 0
                    total_credit = 0
                    total_balance = 0
                    initial_balance = self.get_initial_balance(account['account_id'][0], 'account')
                    if initial_balance and self.is_initial_balance:
                        sheet.write(row, 6, header_initial_balance, content_format)
                        sheet.write(row, 9, initial_balance, content_format)
                        row += 1
                        total_balance += initial_balance
                    for move in self.account_move_line_ids.sorted(key=lambda x: x.date).filtered(
                            lambda line: line.account_id.id == account['account_id'][0]):
                        total_debit += move.debit
                        total_credit += move.credit
                        total_balance += (move.debit - move.credit)
                        create_content(row, move, total_balance)
                        row += 1
                    sheet.merge_range(row, 0, row, 6, total, header_format)
                    sheet.write(row, 7, total_debit, header_format)
                    sheet.write(row, 8, total_credit, header_format)
                    sheet.write(row, 9, round(total_balance, 2), header_format)
                    row += 2

        workbook.close()
        output.seek(0)
        self.write({'excel_sheet': base64.encodebytes(output.getvalue())})

        return {
            'type': 'ir.actions.act_url',
            'name': report_name,
            'url': '/web/content/partner.account.report.wizard/%s/excel_sheet/{}.xlsx?download=true'.format(
                report_name) % (self.id),
            'target': 'self'
        }
