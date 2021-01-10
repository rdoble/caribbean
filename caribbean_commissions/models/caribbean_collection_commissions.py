# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp
from datetime import time, datetime
from openerp.exceptions import Warning, ValidationError
import logging

_logger = logging.getLogger(__name__)

class CaribbeanCollectionCommissionSetting(models.Model):
    _name = 'caribbean.collection.commission.setting'
    _description = 'Configuraciones de comisiones por cobros'

    name = fields.Char(string='Nombre Comisión')
    initial_expiration = fields.Integer(string=u'Días desde')
    top_expiration = fields.Integer(string=u'Días hasta')
    commission = fields.Float(string=u'Comisión (%)', digits=(12,3))