odoo.define('henca_fiscal_print.screens', function (require) {
  "use strict";

  var FormController = require('web.FormController');

  FormController.include({
    ipf_request: async (type, uri, ipf_invoice=undefined) => {
      const request = {
        type,
        url: uri,
        contentType: "application/json",
        dataType: "json"
      };

      if (ipf_invoice) {
        request.data = JSON.stringify(ipf_invoice);
      }

      const response = await $.ajax(request)
        .catch(error => console.log(error));

      return response;
    },

    _onButtonClicked: async event => {
      if (event.data.attrs.custom === "fiscal_print") {
        const {
          number,
          sale_fiscal_type,
          user_id,
          reference,
          partner_id,
          partner_vat,
          invoice_line_ids,
          ipf_host,
          payment_ids,
          amount_total,
          comment,
          ipf_type,
          ipf_print_copy_number
        } = event.data.record.data;

        const comments_array = [];
        if (comment) {
          const normalized_comment = comment
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "")
            .replace(/['"]+/g, '');

          const comment_words_array = normalized_comment.split(' ');
          let comments_array_index = 0;
          let new_string_line = '';

          for(let i=0; i < comment_words_array.length; i++){
            if (comments_array[comments_array_index]) {
              new_string_line = comments_array[comments_array_index] + ' ' + comment_words_array[i];
              if (new_string_line.length > 40) {
                comments_array_index++;
                if (comments_array_index == 9) break;
                comments_array[comments_array_index] = comment_words_array[i]
              } else {
                comments_array[comments_array_index] = new_string_line;
              }
            } else {
              comments_array[comments_array_index] = comment_words_array[i];
            }
          }
        }

        const ipf_invoice = {
          type: sale_fiscal_type,
          cashier: user_id.data.id,
          subsidiary: 1,
          ncf: "00000000" + reference,
          client: partner_id.data.display_name.split("\n")[0],
          rnc: partner_vat || '',
          items: invoice_line_ids.data.map(({ data: { name, quantity, price_unit, tax_amount, tax_amount_type } }) => {
            if (tax_amount_type === 'percent') {
              price_unit = price_unit * (tax_amount / 100.0 + 1)
            }
            return {
              description: name
                .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
                .replace(/['"]+/g, '')
                .slice(0, 40),
              quantity: quantity,
              price: price_unit.toFixed(2),
              itbis: tax_amount,
            }
          }),
          payments: payment_ids.data.length > 0 ? payment_ids.data.map(({ data: { amount, payment_form, journal_id }  }) => ({
            type: payment_form === "bank" ? "check" : payment_form,
            amount: amount.toFixed(2),
            description: journal_id.data.display_name
          })) : [{ type: "credit", description: "Credito", amount: amount_total }],
          comments: [
            'No. Documento:' + ' ' + number,
            ...comments_array
          ]
        }

        if (ipf_print_copy_number == 1 && ipf_type === 'epson') {
          ipf_invoice.copy = true
        } else if (ipf_print_copy_number == 2 && ipf_type === 'epson') {
          ipf_invoice.copy2 = true
        }

        console.log(ipf_invoice);
        if (ipf_host) {
          const response = await this.ipf_request('POST', `${ipf_host}/invoice`, ipf_invoice);
          console.log('IPF Response:', response)
    
          if (ipf_type === 'bixolon') {
            let copy_response;
            for(let i=0; i < ipf_print_copy_number; i++){
              copy_response = await this.ipf_request('POST', `${ipf_host}/invoice/last`);
              console.log(`IPF copy response number ${i}:`, copy_response)
            }
          }
        }
      } else if (event.data.attrs.custom === "z_close_print") {
        const { host } = event.data.record.data;
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
