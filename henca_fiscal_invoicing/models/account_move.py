# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date


class AccountMove(models.Model):
    _inherit = "account.move"

    fiscal_nif = fields.Char("NIF", default="false", copy=False)

    fiscal_printed = fields.Boolean(string='Imprimido Fiscal',copy=False)
    
    show_print_fiscal = fields.Boolean(string='Mostrar boton para imprimir fiscal ?',
     compute='_compute_fiscal_printer',copy=False)
    
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
        compute="_compute_invoice_date_currency_rate",
        default=0.0,
    )

    dop_currency_id = fields.Many2one(
        comodel_name='res.currency',
        default=lambda self: self.env.ref('base.DOP').id,
        string='DOP Currency ID',
        readonly=True
    )

    def _compute_invoice_date_currency_rate(self):
        # import web_pdb;web_pdb.set_trace()  #Break down!
        for move in self:
            if move.dop_currency_id.id != move.currency_id.id:
                # If date not specified on the invoice default to today's date
                invoice_date = move.invoice_date if move.invoice_date else date.today()
                currency_rates = self.env['res.currency.rate'].search([
                    ('company_id', '=', move.company_id.id),
                    ('currency_id', '=', move.currency_id.id),
                    ('name', '<=', invoice_date)
                ], order='name asc')

                rate = currency_rates[-1].rate if currency_rates else 1
                move.invoice_date_currency_rate = rate
            else:
                move.invoice_date_currency_rate = 0.0

    def _compute_fiscal_printer(self):
        for move in self:
            ipf_printer_id = move.env['ipf.printer.config'].search([
                ('user_ids', '=', move.user_id.id)
            ])
            move.ipf_printer_id = ipf_printer_id.id if ipf_printer_id else False

            if move.type == 'out_invoice' or move.type == 'out_refund':
                move.show_print_fiscal = True
            else:
                move.show_print_fiscal = False

            for line in move.line_ids:
                if line.tax_amount_type == False:
                    line._compute_tax_amount_and_type()


            # move._compute_payments_widget_reconciled_info()


    @api.model
    def action_invoice_printed(self, invoice_id,fiscal_nif):
        if invoice_id:
            invoice = self.search([('id','=',invoice_id)])
            if invoice:
                invoice.write({'fiscal_printed': True, 'fiscal_nif': fiscal_nif})
    
    @api.depends('type', 'line_ids.amount_residual')
    def _get_reconciled_info_JSON_values(self):
        payment_vals = super(AccountMove, self)._get_reconciled_info_JSON_values()
        if self.type in ['out_invoice', 'out_refund']:
            for payment in payment_vals:
                if payment['account_payment_id']:
                    payment_obj = self.env['account.payment'].browse(
                        payment['account_payment_id'])
                    payment_form = payment_obj.journal_id.l10n_do_payment_form
                    journal_name = payment_obj.journal_id.name
                    payment['ipf_payment_form'] = payment_form or False
                    payment['ipf_payment_description'] = journal_name
                elif payment['move_id']:
                    ref = payment['ref']
                    payment_form = 'credit_note' if 'B04' in ref else 'other'
                    payment['ipf_payment_form'] = payment_form or False
                    payment['ipf_payment_description'] = ref
        return payment_vals

    def ipf_fiscal_print(self):
        pass


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    invoice_date_currency_rate = fields.Float(
        related='move_id.invoice_date_currency_rate',
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

    @api.depends('tax_ids', 'product_id', 'price_unit')
    def _compute_tax_amount_and_type(self):
        for line in self:
            try:
          
                if line.tax_ids and line.price_unit:
                    tax_amount_list = [18, 13, 11, 8, 5, 0]
                    tax_list = [tax.amount for tax in line.tax_ids]
                    tax_match = [i for i, j in zip(tax_list, tax_amount_list)
                                if i == j]
        
                    if tax_match:
                        for t in line.tax_ids:
                            if t.amount == tax_match[0]:
                                line.tax_amount_type = t.amount_type
                                line.tax_amount = t.amount
                else:
                    line.tax_amount_type = "except"
                    line.tax_amount = 0.0
            except:
                line.tax_amount_type = "except"
                line.tax_amount = 0.0

