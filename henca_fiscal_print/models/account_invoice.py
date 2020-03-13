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

    ipf_type = fields.Selection(
        string="IPF Impresora",
        readonly=True,
        related='ipf_printer_id.ipf_type'
    )

    ipf_print_copy_number = fields.Integer(
        string="Numero de Copias",
        related='ipf_printer_id.print_copy_number'
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

    @api.model
    def _get_payments_vals(self):
        payment_vals = super(AccountInvoice, self)._get_payments_vals()
        for payment in payment_vals:
            if payment['account_payment_id']:
                account_payment = self.env['account.payment'].browse(payment['account_payment_id'])
                payment_form = account_payment.journal_id.payment_form 
                payment_description = account_payment.journal_id.display_name
            elif payment['invoice_id']:
                payment_description = payment['ref']
                payment_form = 'credit_note' if 'B04' in payment_description else 'other'
            payment['ipf_payment_form'] = payment_form
            payment['ipf_payment_description'] = payment_description
        return payment_vals

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
    