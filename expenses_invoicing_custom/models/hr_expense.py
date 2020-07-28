# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

try:
    from stdnum.do import ncf as ncf_validation
except (ImportError, IOError) as err:
    _logger.debug(err)


class HrExpense(models.Model):
    _inherit = 'hr.expense'

    supplier_id = fields.Many2one('res.partner', string='Proveedor')
    invoice_ref = fields.Char('Referencia Factura')
    requires_ncf = fields.Boolean('Requiere NCF', default=False)

    @api.onchange('reference')
    def _onchange_reference_validation(self):
        NCF = self.reference if self.reference else None
        if NCF:
            if len(NCF) != 11:
                raise ValidationError("El NCF debe tener 11 caracteres.")

            elif NCF[-10:-8] == '02' or NCF[1:3] == '32':
                raise ValidationError(
                    "NCF *{}* NO corresponde con el tipo de documento\n\n"
                    "No puede registrar Comprobantes Consumidor Final (02)"
                    .format(NCF))
            elif not ncf_validation.is_valid(NCF):
                raise ValidationError(
                    "NCF mal digitado\n\n"
                    "El comprobante *{}* no tiene la estructura correcta "
                    "valide si lo ha digitado correctamente".format(NCF))

    @api.multi
    def action_submit_expenses(self):
        res = super(HrExpense, self).action_submit_expenses()
        res['context']['default_requires_ncf'] = self.requires_ncf

        if not self.requires_ncf:
            journal_id = self.env['account.journal'].search([('purchase_type', '=', 'informal')], limit=1)
            if journal_id:
                res['context']['default_journal_id'] = journal_id.id
        return res


class HrExpenseSheet(models.Model):
    _inherit = 'hr.expense.sheet'

    invoice_ids = fields.One2many('account.invoice', 'expense_sheet_id', string='Facturas')
    requires_ncf = fields.Boolean('Requiere NCF', default=False)

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
                    'name': expense.invoice_ref,
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
