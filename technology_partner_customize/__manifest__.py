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
    'name': "Technology Partners Customization",

    'summary': """
        This App will Customize Some Details to Technology Partners Company.
        """,

    'description': """
       This App will Customize Some Details to Technology Partners Company.
    """,

    'author': "Abdullah Elyamani",
    'website': "abdullahelyamani@gmail.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['sale_purchase'],

    # always loaded
    'data': [
        'views/sale_order_views.xml',
        'views/purchase_order_views.xml',
        'views/account_move_views.xml',
        'views/product_supplierinfo_views.xml',
    ],

    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
