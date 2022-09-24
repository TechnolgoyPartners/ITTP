# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo,
#    Copyright (C) 2022 dev: Abdullah Elyamani.
#    Mob. +20 1011002165
#    Email. abdullahelyamani@gmail.com
#
##############################################################################
{
    'name': "Partner Account Report",

    'summary': """
        This App Allow User to create account report for partner.
        """,

    'description': """
        This App For Allow you to create account report for partner:
        1- Can Filter with many partner.
        2- Can Filter with many account.
        3- Can Filter with many journal.
        4- Can Filter with many analytic account.
        5- Can Filter with many analytic tag account.
        6- Can View report with pdf, html, excel.
    """,

    'author': "Abdullah Elyamani",
    'website': "abdullahelyamani@gmail.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['account'],

    # always loaded
    'data': [
        'security/partner_account_security.xml',
        'security/ir.model.access.csv',
        'report/partner_account_report.xml',
        'report/partner_account_report_template.xml',
        'wizard/partner_account_report_wizard_views.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
