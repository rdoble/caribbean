# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    fiscal_nif = fields.Char("NIF", default="false", copy=False)

    ipf_printer_id = fields.Many2one(
        string='Impresora Fiscal',
        comodel_name='ipf.printer.config',
        compute='_get_fiscal_printer'
    )

    ipf_host = fields.Char(
        string='IPF Host',
        related='ipf_printer_id.host'
    )

    def _get_fiscal_printer(self):
        ipf_printer_id = self.env['ipf.printer.config'].search([
            ('user_ids', '=', self.user_id.id)
        ])

        if ipf_printer_id:
            self.ipf_printer_id = ipf_printer_id[0]

    partner_vat = fields.Char(
        string='RNC',
        related='partner_id.vat',
        readonly=True
    )

    def ipf_fiscal_print(self):
        print('IPF FISCAL PRINT IS FIRING!')

    