# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    fiscal_nif = fields.Char("NIF", default="false", copy=False)

    fiscal_printed = fields.Boolean(string='Imprimido Fiscal', copy=False)

    show_print_fiscal = fields.Boolean(string='Mostrar boton para imprimir fiscal ?',
                                       compute='_compute_fiscal_printer', copy=False)

    ipf_printer_id = fields.Many2one(
        string='Impresora Fiscal',
        comodel_name='ipf.printer.config',
        compute='_compute_fiscal_printer'
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

    partner_vat = fields.Char(
        string='RNC',
        related='partner_id.vat',
        readonly=True
    )

    invoice_date_currency_rate = fields.Float(
        string="Tasa de Cambio Fecha Factura",
        compute="_get_invoice_date_currency_rate",
        default=0.0,
    )

    dop_currency_id = fields.Many2one(
        comodel_name='res.currency',
        default=lambda self: self.env.ref('base.DOP').id,
        string='DOP Currency ID',
        readonly=True
    )

    @api.depends('date_invoice', 'currency_id')
    def _get_invoice_date_currency_rate(self):
        if self.dop_currency_id.id != self.currency_id.id:
            # If date not specified on the invoice default to today's date
            invoice_date = self.date_invoice if self.date_invoice else date.today()
            currency_rates = self.env['res.currency.rate'].search([
                ('company_id', '=', self.company_id.id),
                ('currency_id', '=', self.currency_id.id),
                ('name', '<=', invoice_date)
            ], order='name asc')

            rate = currency_rates[-1].rate if currency_rates else 1
            self.invoice_date_currency_rate = rate

    def _compute_fiscal_printer(self):
        for move in self:
            ipf_printer_id = move.env['ipf.printer.config'].search([
                ('user_ids', '=', move.user_id.id)
            ])

            if len(ipf_printer_id) > 1:
                ipf_printer_id = ipf_printer_id[0]


            move.ipf_printer_id = ipf_printer_id.id if ipf_printer_id else False

            if move.type == 'out_invoice' or move.type == 'out_refund':
                move.show_print_fiscal = True
            else:
                move.show_print_fiscal = False

            for line in move.invoice_line_ids:
                if line.tax_amount_type == False:
                    line._compute_tax_amount_and_type()

    @api.model
    def action_invoice_printed(self, invoice_id, fiscal_nif):
        if invoice_id:
            invoice = self.search([('id', '=', invoice_id)])
            if invoice:
                invoice.write(
                    {'fiscal_printed': True, 'fiscal_nif': fiscal_nif})

    @api.model
    def _get_payments_vals(self):
        payment_vals = super(AccountInvoice, self)._get_payments_vals()
        if self.type in ['out_invoice', 'out_refund']:
            for payment in payment_vals:
                payment_form = False
                payment_description = False
                if payment['account_payment_id']:
                    account_payment = self.env['account.payment'].browse(
                        payment['account_payment_id'])
                    payment_form = account_payment.journal_id.payment_form
                    payment_description = account_payment.journal_id.display_name
                    payment['ipf_payment_form'] = payment_form
                    payment['ipf_payment_description'] = payment_description
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

    invoice_date_currency_rate = fields.Float(
        related='invoice_id.invoice_date_currency_rate',
        string='Tasa',
    )
    tax_amount_type = fields.Char(
        string='Tax Computation',
        compute='_compute_tax_amount_and_type',
        store=True,
        readonly=True,
    )
    tax_amount = fields.Float(
        string='Tax Amount',
        compute='_compute_tax_amount_and_type',
        store=True,
        readonly=True,
    )

    @api.onchange('invoice_line_tax_ids', 'product_id', 'price_unit')
    def _compute_tax_amount_and_type(self):
        for record in self:
            try:
                if record.invoice_line_tax_ids and record.price_unit:
                    tax = record.invoice_line_tax_ids[0]
                    tax_amount_int = int(tax.amount)
                    tax_amount = tax_amount_int if tax_amount_int in [
                        18, 13, 11, 8, 5, 0] else 0
                    record.update({
                        'tax_amount_type': tax.amount_type,
                        'tax_amount': tax_amount
                    })
            except:
                line.tax_amount_type = "except"
                line.tax_amount = 0


class AccountPayment(models.Model):
    _inherit = "account.payment"

    payment_form = fields.Selection(
        string='Payment Form',
        related='journal_id.payment_form'
    )
