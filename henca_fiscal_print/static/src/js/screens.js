odoo.define('henca_fiscal_print.screens', function (require) {
  "use strict";

  var FormController = require('web.FormController');

  FormController.include({
    _onButtonClicked: function (event) {
      if (event.data.attrs.custom === "fiscal_print") {
        var {
          sale_fiscal_type,
          user_id,
          reference,
          partner_id,
          partner_vat,
          invoice_line_ids,
          ipf_host,
          payment_ids,
          amount_total
        } = event.data.record.data;

        var ipf_invoice = {
          type: sale_fiscal_type,
          cashier: user_id.data.id,
          subsidiary: 1,
          ncf: "00000000" + reference,
          client: partner_id.data.display_name.split("\n")[0],
          rnc: partner_vat,
          items: invoice_line_ids.data.map(({ data: { name, quantity, price_unit, tax_amount, tax_amount_type } }) => {
            if (tax_amount_type === 'percent') {
              price_unit = price_unit * (tax_amount / 100.0 + 1)
            }
            return {
              description: name,
              quantity: quantity,
              price: price_unit,
              itbis: tax_amount,
            }
          }),
          payments: payment_ids.data.length > 0 ? payment_ids.data.map(({ data: { amount, payment_form, journal_id }  }) => ({
            type: payment_form === "bank" ? "check" : payment_form,
            amount: amount,
            description: journal_id.data.display_name
          })) : [{ type: "credit", description: "Credito", amount: amount_total }]
        }
        if (ipf_host) {
          $.ajax({
              type: 'POST',
              url: ipf_host + "/invoice",
              data: JSON.stringify(ipf_invoice),
              contentType: "application/json",
              dataType: "json"
          }).done(function (response) {
              console.log(response);
          }).fail(function (response) {
              console.log(response);
          });
        }

      } else if (event.data.attrs.custom === "z_close_print") {
        var { host } = event.data.record.data;
        $.ajax({
          type: 'GET',
          url: host + "/zclose/print",
        }).done(function (response) {
            console.log(response);
        }).fail(function (response) {
            console.log(response);
        });
      }
      this._super(event);
    },
  });

});