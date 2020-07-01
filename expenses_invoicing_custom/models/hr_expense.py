# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrExpense(models.Model):
    _inherit = 'hr.expense'

    supplier_id = fields.Many2one('res.partner', string='Proveedor')


class HrExpenseSheet(models.Model):
    _inherit = 'hr.expense.sheet'

    invoice_ids = fields.One2many('account.invoice', 'expense_sheet_id', string='Facturas')

    @api.multi
    def action_expense_invoice_create(self):
        ACCOUNT_INVOICE = self.env['account.invoice']

        suppliers = list(set(self.expense_line_ids.mapped('supplier_id')))

        for supplier in suppliers:
            for expense in self.expense_line_ids.filtered(lambda eli: eli.supplier_id == supplier):

                product = expense.product_id
                vals = {
                    'partner_id': expense.supplier_id.id,
                    'type': 'in_invoice',
                    'journal_id': self.journal_id.id,
                    'reference': expense.reference,
                    'date_invoice': expense.date,
                    'expense_sheet_id': self.id,
                    'currency_id': self.currency_id.id,
                    'invoice_line_ids': [(0, 0, {
                        'product_id': product.id,
                        'name': product.name + '\n' + expense.name,
                        'account_id': product.property_account_expense_id.id or product.categ_id.property_account_expense_categ_id.id,
                        'quantity': expense.quantity,
                        'uom_id': product.uom_id.id,
                        'price_unit': expense.unit_amount,
                        'invoice_line_tax_ids': [(6, 0, expense.tax_ids.ids)]
                    })]
                }

                ACCOUNT_INVOICE += ACCOUNT_INVOICE.create(vals)

        self.write({'state': 'post'})

    @api.multi
    def action_view_invoice_tree(self):
        invoices = self.invoice_ids
        action = self.env.ref('account.action_vendor_bill_template').read()[0]
        action['domain'] = "[('id', 'in', " + str(invoices.ids) + ")]"
        return action
