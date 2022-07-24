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
    'name': "Multiple Purchase",

    'summary': """
        This Module Allowed User to create Purchase Order from Sale Order.
        """,

    'description': """
       This Module Allowed User to create Purchase Order from Sale Order.
    """,

    'author': "Abdullah Elyamani",
    'website': "abdullahelyamani@gmail.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['sale', 'purchase', 'multiple_quotation_handler', 'technology_partner_customize'],

    # always loaded
    'data': [
        'views/sale_order_views.xml',
        'views/purchase_order_views.xml',
    ],

    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
