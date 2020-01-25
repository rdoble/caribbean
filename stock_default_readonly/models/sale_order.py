# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp
from openerp.exceptions import Warning, ValidationError
import logging
import datetime

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    warehouse_id = fields.Many2one( 'stock.warehouse', string='Warehouse', required=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)], 'sale': [('readonly', True)], 'done': [('readonly', True)], 'cancel': [('readonly', True)]})
    
    @api.onchange('user_id')
    def _default_warehouse_id(self):
        
        if self.user_id and self.user_id.stock_id :
           self.warehouse_id = self.user_id.stock_id.id
        else:
            raise Warning ("Usuario no tiene almacen asignado, por favor cominicarse con el administrador del sistema")