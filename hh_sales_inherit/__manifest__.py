# -*- coding: utf-8 -*-
{
    'name': "hh_sales_inherit",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management', 'account_accountant'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/sales_quotation_template.xml',
        'views/purchase_quotation_template.xml',
        'views/purchase_shipping_term.xml',
        'views/sales_shipping_term.xml',
        'views/sale_order_inherit.xml',
        'views/templates.xml',
        'data/purchase_order_custom_sequence.xml',
        'views/purchase_order_inherit.xml',
        'wizard/tax_reporting_wizard.xml',
        'report/taxes_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
