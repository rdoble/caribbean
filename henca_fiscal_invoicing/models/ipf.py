# -*- coding: utf-8 -*-
from odoo import models, fields, api
import odoo.addons.decimal_precision as dp
import base64


class IpfPrinterConfig(models.Model):
    _name = 'ipf.printer.config'

    IPF_TYPE = [
        ('epson', 'EPSON TM-T88v'),
        ('bixolon', 'BIXOLON SRP-350')
    ]

    name = fields.Char(
        string="Descripcion",
        required=True
    )
    ipf_type = fields.Selection(
        string="IPF Impresora",
        required=True,
        selection=IPF_TYPE,
        default='epson'
    )
    host = fields.Char(
        string="Host",
        required=True
    )
    user_ids = fields.Many2many(
        comodel_name='res.users',
        string="Usuarios",
        required=True
    )
    print_copy = fields.Boolean(
        string="Imprimir con copia",
        default=False
    )
    print_copy_number = fields.Integer(
        string="Numero de Copias",
        required=True,
        default=0
    )
    subsidiary = fields.Many2one(
        comodel_name="res.company",
        string="Sucursal",
        required=False
    )
    active = fields.Boolean(
        string="Active",
        default=True
    )
    serial = fields.Char(
        string="Serial de la impresora",
        readonly=True
    )

    daily_book_ids = fields.One2many(
        "ipf.daily.book", "printer_id", string="Libros diarios")

    def toggle_active(self):
        self.active = not self.active

    def z_close_print(self):
        pass

    def x_close_print(self):
        pass

    def get_state(self):
        pass

    def get_advance_paper(self):
        pass
    
    def get_x(self):
        pass
    
    def get_new_shift_print(self):
        pass

    def get_printer_information(self):
        pass

    def get_cut_paper(self):
        pass

    def get_daily_book(self):
        pass
    
    def get_information_day(self):
        pass

    def get_information_shift(self):
        pass
    
    def get_serial(self):
        pass
        

    @api.model
    def get_user_printer(self):
        return self.search([("user_ids", "=", self.env.uid)])

    @api.model
    def get_ipf_host(self, get_id=False):
        printer = False

        if self._context.get("active_model", False) == "ipf.printer.config":
            printer = self.browse(self._context["active_id"])
        else:
            printer = self.get_user_printer()

        if printer:
            if get_id:
                return printer.id
            else:
                return {"host": printer.host}
        else:
            raise exceptions.Warning("Las impresoras fiscales no estan configuradas!")

    def set_book_totals(self, book):
        book_header_sun = [0, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
        daily_book_row = base64.b64decode(book.book).decode('utf-8').split("\n")

        for row in daily_book_row:
            field_list = row.split("||")
            if field_list[0] == "1":
                book_header_sun[0] += int(field_list[3]) if field_list[3] else 0
                book_header_sun[1] += float(field_list[4]) if field_list[4] else 0.00
                book_header_sun[2] += float(field_list[5]) if field_list[5] else 0.00
                book_header_sun[3] += float(field_list[11]) if field_list[11] else 0.00
                book_header_sun[4] += float(field_list[12]) if field_list[12] else 0.00
                book_header_sun[5] += float(field_list[14]) if field_list[14] else 0.00
                book_header_sun[6] += float(field_list[15]) if field_list[15] else 0.00
                book_header_sun[7] += float(field_list[17]) if field_list[17] else 0.00
                book_header_sun[8] += float(field_list[18]) if field_list[18] else 0.00
                book_header_sun[9] += float(field_list[20]) if field_list[20] else 0.00
                book_header_sun[10] += float(field_list[21]) if field_list[21] else 0.00

        values = {
            "doc_qty": book_header_sun[0],
            "total": book_header_sun[1],
            "total_tax": book_header_sun[2],
            "final_total": book_header_sun[3],
            "final_total_tax": book_header_sun[4],
            "fiscal_total": book_header_sun[5],
            "fiscal_total_tax": book_header_sun[6],
            "ncfinal_total": book_header_sun[7],
            "ncfinal_total_tax": book_header_sun[8],
            "ncfiscal_total": book_header_sun[9],
            "ncfiscal_total_tax": book_header_sun[10],
        }

        return book.write(values)

    @api.model
    def save_book(self, new_book, serial, bookday):
        printer_id = self.get_ipf_host(get_id=True)
        date = bookday.split("-")
        filename = "LV{}{}{}.000".format(date[0][2:4], date[1], date[2])

        book = self.env["ipf.daily.book"].search([('serial', '=', serial), ('date', '=', bookday)])
        if book:
            book.unlink()
        values = {"printer_id": printer_id, "date": bookday, "book": base64.b64encode(new_book.encode("utf-8")), "serial": serial,
                  "filename": filename}

        new_book = self.env["ipf.daily.book"].create(values);

        self.set_book_totals(new_book)

        return True

    @api.model
    def save_serial_printer(self, serial):
        printer_id = self.get_ipf_host(get_id=True)
        self.browse(printer_id).write({'serial':serial})
        return True




class ipf_daily_book(models.Model):
    _name = "ipf.daily.book"
    _order = "date"

    printer_id = fields.Many2one(
        "ipf.printer.config", string="Printer", readonly=True)
    subsidiary = fields.Many2one(
        "", string="Sucursal", related="printer_id.subsidiary")
    date = fields.Date("Fecha", readonly=True)
    serial = fields.Char("Serial", readonly=True)
    book = fields.Binary("Libro diario", readonly=True)
    filename = fields.Char("file name", readonly=True)

    doc_qty = fields.Integer(
        "Transacciones", digits=dp.get_precision('Account'))
    total = fields.Float("Total", digits=dp.get_precision('Account'))
    total_tax = fields.Float("Total Itbis", digits=dp.get_precision('Account'))
    final_total = fields.Float(
        "Final total", digits=dp.get_precision('Account'))
    final_total_tax = fields.Float(
        "Final Itbis total", digits=dp.get_precision('Account'))
    fiscal_total = fields.Float(
        "Fiscal total", digits=dp.get_precision('Account'))
    fiscal_total_tax = fields.Float(
        "Fiscal Itbis total", digits=dp.get_precision('Account'))
    ncfinal_total = fields.Float(
        "NC final total", digits=dp.get_precision('Account'))
    ncfinal_total_tax = fields.Float(
        "NC final Itbis total", digits=dp.get_precision('Account'))
    ncfiscal_total = fields.Float(
        "NC fiscal total", digits=dp.get_precision('Account'))
    ncfiscal_total_tax = fields.Float(
        "NC fiscal Itbis total", digits=dp.get_precision('Account'))
