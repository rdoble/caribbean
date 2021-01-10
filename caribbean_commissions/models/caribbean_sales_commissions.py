# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp
from datetime import time, datetime
from openerp.exceptions import Warning, ValidationError
import logging

_logger = logging.getLogger(__name__)

class CaribbeanSalesCommissionSetting(models.Model):
    _name = 'caribbean.sales.commission.setting'
    _description = 'Configuraciones de comisiones'

    name = fields.Char(string='Nombre Comisión')
    initial_amount = fields.Float(string=u'Monto Inicial')
    top_amount = fields.Float(string=u'Monto Máximo')
    commission_amount = fields.Float(string=u'Monto Comisión')
    is_percent = fields.Boolean(string=u'En porciento')
    equipment_category_id = fields.Many2one('product.category', string=u'Categoria de Equipos')
    equipment_category_ids = fields.Many2many(string=u'Categorias de Equipos', comodel_name='product.category', relation='csc_pc_rel', column1='commission_id', column2='categ_id')
    equipment_equipment_margin = fields.Many2many(string=u'Comisiones por Magen (%)', comodel_name='caribbean.sales.commission.equipment.margin', relation='csc_em_rel', column1='commission_id', column2='equipment_margin_id')
    collection_commission_id = fields.Many2many(string=u'Comisiones de Cobros', comodel_name='caribbean.collection.commission.setting', relation='csc_cc_rel', column1='commission_id', column2='collection_commission_id')

class CaribbeanSalesCommissionEquipmentMargin(models.Model):
    _name = 'caribbean.sales.commission.equipment.margin'
    _description = 'Configuraciones de comisiones de equipos segun el margen de beneficio'

    name = fields.Char(string='Margen')
    initial_margin = fields.Float(string=u'Margen inicial (%)')
    top_margin = fields.Float(string=u'Margen Máximo (%)')
    commission = fields.Float(string=u'Comisión (%)')
    
class CaribbeanHrEmployeeCommissions(models.Model):
    _inherit = 'hr.employee'
    _description = 'Configuración de comisiones a empleados'

    commission_id = fields.Many2one('caribbean.sales.commission.setting', string=u'Comisión')