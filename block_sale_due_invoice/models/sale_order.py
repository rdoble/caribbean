# © 2020 Anthony Martinez <anthonyame02@gmail.com>

# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# See <https://www.gnu.org/licenses/>.

import logging

from odoo import models, fields, api, _
from datetime import datetime
from datetime import date
from odoo.exceptions import UserError, ValidationError, Warning

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    sales_is_blocked = fields.Boolean(string='Bloquear ventas', default=True,
                                      help="Bloquear ventas cuando el cliente tiene facturas vencidas pendientes de pago ")
    limit_amount = fields.Float(string='Límite de Crédito')


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def action_confirm(self, values):

        res = super(SaleOrder, self).action_confirm()

        for rec in self:

            if rec.partner_id.sales_is_blocked:

                invoices = self.env['account.invoice'].search([('partner_id', '=', rec.partner_id.id), ('state', 'in', [
                    'open', 'in_payment']), ('type', '=', 'out_invoice')])
                current_date = str(datetime.today())[0:10]
                total_amount = 0.0

                for inv in invoices:

                    total_amount += total_amount

                    d1 = date(int(current_date.split(
                        "-")[0]), int(current_date.split("-")[1]), int(current_date.split("-")[2]))
                    d2 = date(int(str(inv.date_due).split(
                        "-")[0]), int(str(inv.date_due).split("-")[1]), int(str(inv.date_due).split("-")[2]))
                    payterm_day = 0

                    for payterm in inv.payment_term_id.line_ids:
                        payterm_day = payterm.days

                    if (total_amount + rec.amount_total) > rec.partner_id.limit_amount and (d1-d2).days > payterm_day:
                        raise Warning(_("El cliente {} tiene pagos vencidos pendientes".format(inv.partner_id.name)))

        return res
