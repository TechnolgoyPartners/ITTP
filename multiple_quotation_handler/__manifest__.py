# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2018-TODAY NIKHIL KRISHNAN(nikhilkrishnan0101@gmail.com).
#    Author: Nikhil krishnan(nikhilkrishnan0101@gmail.com)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Multiple Quotation Handler',
    'version': '11.0.1.0.0',
    'summary': """We Can Handle Multiple Quotations in a Quotation, and convert a single Quotation into Sale Order.""",
    'description': """For best Negotiations with clients we can sent multiple Quotations at a time amd convert the best 
    Quotation into Sale Order,""",
    'author': 'NIKHIL KRISHNAN',
    'company': '',
    'website': '',
    'category': 'Sales Management',
    'depends': ['sale', 'sale_management'],
    'license': 'LGPL-3',
    'data': [
        'security/security_data.xml',
        'security/ir.model.access.csv',
        'data/multi_quotation_sequence.xml',
        'views/multi_quotation_handler.xml',
        'wizard/quotations_selector_wizard.xml',
        'report/sale_report_templates.xml',
        'data/mail_template_multi_quotation.xml',

    ],
    'demo': [],
    'images': ['static/description/banner.jpg'],
    'installable': True,
    'auto_install': False,
}
