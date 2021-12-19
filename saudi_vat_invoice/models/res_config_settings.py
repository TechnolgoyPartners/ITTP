# -*- coding: utf-8 -*-
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2020. All rights reserved.

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    qr_code_generation_config = fields.Selection([
        ('auto', 'Generate QR Code when Invoice validate/post'),
        ('manual', 'Manually Generate')], string="QR Code Generation Configuration",
        required=True, default='auto', config_parameter='saudi_vat_invoice.qr_code_generation_config')
