# -*- coding: utf-8 -*-

from odoo import api, fields, models

class ResUsers(models.Model):
    _inherit = 'res.users'

    stock_id = fields.Many2one('stock.warehouse', string='Almacen')
