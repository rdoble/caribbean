odoo.define('henca_fiscal_print.screens', function (require) {
  "use strict";

  var FormController = require('web.FormController');

  FormController.include({
    _onButtonClicked: function (event) {
      if (event.data.attrs.custom === "fiscal_print") {
        console.log('fiscal print button pressed')
        var {
          sale_fiscal_type,
          user_id,
          reference,
          partner_id,
          partner_vat,
          invoice_line_ids,
          ipf_host
        } = event.data.record.data;

        console.log(record)
        var ipf_invoice = {
          type: sale_fiscal_type,
          cashier: user_id.data.id,
          subsidiary: 1,
          ncf: "00000000" + reference,
          client: partner_id.data.display_name,
          rnc: partner_vat,
          items: invoice_line_ids.data.map(({ data: { name, quantity, price_unit } }) => ({
            description: name,
            quantity: quantity,
            price: price_unit,
            itbis: 18,
          }))
        }

        console.log(ipf_host)
        console.log('IPF Invoice:', ipf_invoice)
        if (ipf_ip) {
          $.ajax({
              type: 'POST',
              url: ipf_ip + "/invoice",
              data: JSON.stringify(ipf_invoice),
              contentType: "application/json",
              dataType: "json"
          }).done(function (response) {
              console.log(response);

          }).fail(function (response) {
              console.log(response);
              console.log(JSON.parse(response.responseText));
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
            console.log(JSON.parse(response.responseText));
        });
      }
      this._super(event);
    },
  });

});