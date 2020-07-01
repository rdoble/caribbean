# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    expense_sheet_id = fields.Many2one('hr.expense.sheet', string='Informe de Gasto')
