# -*- coding: utf-8 -*-
# Copyright (C) 2017-Today  Technaureus Info Solutions(<http://technaureus.com/>).
from odoo import api, fields, models

class Partner(models.Model):
    _inherit = 'res.partner'
    
    partner_place_supply = fields.Selection([('abu_dhabi','Abu Dhabi'), ('ajman','Ajman'), ('dubai','Dubai'), ('fujairah','Fujairah'),
                     ('ras_al_khaimah','Ras al-Khaimah'), ('sharjah','Sharjah'), ('umm_al_quwain','Umm al-Quwain')], string= "Place of Supply")
    partner_vat_accounting = fields.Selection(related='company_id.vat_accounting')
    building_number = fields.Char("Building Number")
    district_id = fields.Many2one('res.district',"District")
    building_number_arabic = fields.Char("Building Number")
    district_id_arabic = fields.Char("District")
    additional_no= fields.Char("Additionl Number")
    other_seller_id=fields.Char("Other Seller ID")
    additional_no_arabic = fields.Char("Additionl Number in Arabic")
    other_seller_id_arabic = fields.Char("Other Seller ID in Arabic")