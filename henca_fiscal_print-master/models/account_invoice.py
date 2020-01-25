# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountPayment(models.Model):
    _inherit = "account.payment"

    payment_form = fields.Selection(
        string='Payment Form',
        related='journal_id.payment_form'
    )

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
        pass

class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    tax_amount_type = fields.Char(
        string='Tax Computation',
        compute='_get_tax_amount_and_type',
        readonly=True
    )

    tax_amount = fields.Float(
        string='Tax Amount',
        compute='_get_tax_amount_and_type',
        readonly=True
    )

    @api.onchange(
        'invoice_line_tax_ids',
        'product_id',
        'price_unit'
    )
    def _get_tax_amount_and_type(self):
        for record in self:
            if record.invoice_line_tax_ids and record.price_unit:
                tax = record.invoice_line_tax_ids[0]
                tax_amount_int = int(tax.amount)
                tax_amount = tax_amount_int if tax_amount_int in [18, 13, 11, 8, 5, 0] else 0
                record.update({
                    'tax_amount_type': tax.amount_type,
                    'tax_amount': tax_amount
                })
    