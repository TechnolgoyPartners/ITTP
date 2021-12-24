# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class pos_comm_sale_configuration_settings(models.TransientModel):
	_inherit = "res.config.settings"

	commission_configuration = fields.Selection([('sale_order', 'Commission based on sales order/Point Of Sale'),
										('invoice', 'Commission based on invoice'),
										('payment', 'commission based on payment')
										],string='Generate Commision Entry Based On ',related="company_id.commission_configuration",readonly=False)


class POSResCompanyInherit(models.Model):
	_inherit = 'res.company'

	commission_configuration = fields.Selection([('sale_order', 'Commission based on sales order/Point Of Sale'),
										('invoice', 'Commission based on invoice'),
										('payment', 'commission based on payment')
										],string='Generate Commision Entry Based On ',default='payment')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:                                       

