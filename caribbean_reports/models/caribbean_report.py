# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.addons import decimal_precision as dp
from datetime import time, datetime
from openerp.exceptions import Warning, ValidationError
import base64
import os
import logging

_logger = logging.getLogger(__name__)

class CaribbeanReport(models.Model):
    _name = 'caribbean.report'
    _description = 'Modulo para la creacion de los reportes de Andrickson'

    name = fields.Char(string='Nombre del Reporte')
    report_file_binary = fields.Binary(string='Archivo')
    report_id = fields.Many2one('caribbean.report.setting', string='Reporte')
    report_filename = fields.Char(string='')
    preview_report = fields.Html(string=u'Vista previa del reporte')
    date_from = fields.Date(string=u'Fecha desde', default=fields.Date.context_today)
    date_to = fields.Date(string=u'Fecha hasta', default=fields.Date.context_today)
    
    
    @api.multi
    def btn_generate_report(self):

        report_setting = self.env['caribbean.report.setting'].search([('id', '=', self.report_id.id)])
        _logger.info(self.date_from)

        rs_report = report_setting.executeQuery(self.report_id.query, self.date_from, self.date_to)
        preview_report = ""

         # FORMAMOS EL NUMBRE DEL ARCHIVO
        file_name = "{}.csv".format(self.name)

        file_path = '/tmp/' + file_name
        report_file = open(file_path, 'w')

        for val in rs_report:
            
            if val['reporte']:
                record = ""
                report_file.write(val['reporte'].replace('|',',') + '\n')

                for i in val['reporte'].split('|'):
                    record += "<td style='padding-right:15px'>{}</td>".format(i.replace('"',''))
                
                preview_report += "<tr>{}</tr>".format(record)

        report_file.close()
        report_file = open(file_path, 'rb')
        self.write({'report_file_binary': base64.b64encode(report_file.read()), 'report_filename': file_name})

        self.preview_report = "<table style='width:100%'>{}</table>".format(preview_report)
        return True
           

class CaribbeanReportSetting(models.Model):
    _name = 'caribbean.report.setting'
    _description = 'Configuracion de los reportes Andrickson'

    name = fields.Char(string="Nombre reporte", required=True)
    query = fields.Text(string='Query')
    where = fields.Text(string='Where', default=' ')
    group_by = fields.Text(string='Group By', default=' ')
    order_by = fields.Text(string='Order By', default=' ')
    
    @api.multi
    def executeQuery(self, query, date_from, date_to):

        query = query.replace("OTHER_CONDITION", self.where.format(date_from, date_to))
        query_string = "{} {} {}".format(query, self.group_by, self.order_by)
        
        _logger.info(query_string)
        
        self.env.cr.execute(query_string)
        rs_report = self.env.cr.dictfetchall()

        return rs_report