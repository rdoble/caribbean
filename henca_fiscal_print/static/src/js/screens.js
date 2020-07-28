odoo.define('henca_fiscal_print.screens', function (require) {
  "use strict";
  var FormController = require('web.FormController');

  FormController.include({
    _onButtonClicked: function (event) {
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
          comment,
          ipf_type,
          ipf_print_copy_number,
          residual,
          origin_out,
          payments_widget,
          currency_id,
          dop_currency_id
        } = event.data.record.data;

        console.log(event.data.record.data);
        console.log(event.data.record.data.payments_widget);
        console.log(JSON.parse(payments_widget))


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
          ncf: `00000000${reference}`,
          client: partner_id.data.display_name.split("\n")[0],
          rnc: partner_vat || '',
          items: invoice_line_ids.data.map(({ data: {
            name,
            quantity,
            price_unit,
            tax_amount,
            tax_amount_type,
            discount,
            currency_id,
            invoice_date_currency_rate
          } }) => {
            if (currency_id.data.id != dop_currency_id.data.id) {
              // console.log("Not peso")
              price_unit = 1 / invoice_date_currency_rate * price_unit;
            }
            if (tax_amount_type === 'percent') {
              price_unit *= (tax_amount / 100.0 + 1);
            }
            const ipf_line = {
              description: name
                .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
                .replace(/['"]+/g, '')
                .slice(0, 40),
              quantity: quantity,
              price: price_unit.toFixed(2),
              itbis: tax_amount,
            };

            if (discount) {
              ipf_line.discount = discount;
            }

            return ipf_line;
          }),
          comments: [
            'No. Documento:' + ' ' + number,
            ...comments_array
          ]
        }

        const other_payments = JSON.parse(payments_widget).content;
        console.log(other_payments)
        if (other_payments) {
          ipf_invoice.payments = other_payments.map(({
            amount,
            ipf_payment_form,
            ipf_payment_description
          }) => ({
            amount,
            type: ipf_payment_form === 'bank' ? 'check' :  ipf_payment_form,
            description: ipf_payment_description
          }));
        }

        if (residual) {
          if (!ipf_invoice.payments) {
            ipf_invoice.payments = [];
          }
          ipf_invoice.payments.push({
            type: 'credit',
            description: 'Credito',
            amount: residual
          });
        }

        const items_total = ipf_invoice.items.reduce((total, item) => 
          total + (parseFloat(item.price) * item.quantity)
        , 0);

        const payments_total = ipf_invoice.payments.reduce((total, payment) =>
          total + parseFloat(payment.amount)
        , 0);

        if (items_total != payments_total) {
          const delta_payment = items_total - payments_total
          const last_payment = ipf_invoice.payments.pop();
          last_payment.amount = (parseFloat(last_payment.amount) + delta_payment).toFixed(2);
          ipf_invoice.payments.push(last_payment);
        }

        if (origin_out) {
          ipf_invoice.reference_ncf = `00000000${origin_out}`;
          const origin_prefix = origin_out.slice(0,3);
          switch (origin_prefix) {
            case 'B02':
              ipf_invoice.type = 'final_note';
              break;
            case 'B14':
              ipf_invoice.type = 'special_note';
              break;
            default:
              ipf_invoice.type = 'fiscal_note';
          }
        }

        if (ipf_print_copy_number == 1 && ipf_type === 'epson') {
          ipf_invoice.copy = true
        } else if (ipf_print_copy_number == 2 && ipf_type === 'epson') {
          ipf_invoice.copy2 = true
        }

        console.log(ipf_invoice)
        if (ipf_host) {
          $.ajax({
            type: 'POST',
            url: ipf_host + "/invoice",
            data: JSON.stringify(ipf_invoice),
            contentType: "application/json",
            dataType: "json"
          }).done(function (response) {
            console.log('IPF PRINT RESPONSE:', response);
            if (ipf_type === 'bixolon') {
              for(let i=0; i < ipf_print_copy_number; i++){
                console.log(`Requesting copy number ${i}.`);
                $.ajax({
                  type: 'GET',
                  url: ipf_host + "invoice/last",
                }).done(function (response) {
                  console.log(response);
                }).fail(function (response) {
                  console.log(response);
                });
              }
            }
          }).fail(function (response) {
            console.log(response);
          });
          
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
