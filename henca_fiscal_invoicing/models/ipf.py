# -*- coding: utf-8 -*-
from odoo import models, fields, api
import odoo.addons.decimal_precision as dp
import base64
import calendar
import datetime
import hashlib
from odoo.tools import format_date


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

    extension = fields.Char(
        string="Extension LVM",
        default="001"
    )


    daily_book_ids = fields.One2many(
        "ipf.daily.book", "printer_id", string="Libros diarios")

    monthly_book_ids = fields.One2many(
        "ipf.monthly.book", "printer_id", string="Libros Mensuales")

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
    
    def generate_monthly_book(self):
        pass

    def get_information_day(self):
        pass

    def get_information_shift(self):
        pass
    
    def get_serial(self):
        pass
    
    def get_daily_book_by_date(self):
        pass
        

    @api.model
    def get_user_printer(self):
        printer = self.search([("user_ids", "=", self.env.uid)])
        if printer:
            if len(printer) > 1:
                printer = printer[0]
        return printer

    @api.model
    def get_ipf_host(self, get_id=False):
        printer = False

        if self._context.get("active_model", False) == "ipf.printer.config":
            printer = self.browse(self._context["active_id"])
        else:
            printer = self.get_user_printer()

        if printer:
            if len(printer) > 1:
                printer = printer[0]

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


    def get_books_totals(self, daily_books):
        book_header_sun = [0, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,0.00, 0.00, 0.00, 0.00, 0.00]

    
        for book in daily_books:
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
                    book_header_sun[11] += float(field_list[6]) if field_list[6] else 0.00
                    book_header_sun[12] += float(field_list[7]) if field_list[7] else 0.00
                    book_header_sun[13] += float(field_list[8]) if field_list[8] else 0.00
                    book_header_sun[14] += float(field_list[9]) if field_list[9] else 0.00
                    book_header_sun[15] += float(field_list[10]) if field_list[10] else 0.00
            
        
        
        values = {
            "doc_qty": book_header_sun[0] if book_header_sun[0] > 0 else "",
            "total": book_header_sun[1] if book_header_sun[1] > 0 else "",
            "total_tax": book_header_sun[2] if book_header_sun[2] > 0 else "",
            "total_tax_rate1": book_header_sun[11] if book_header_sun[11] > 0 else "",
            "total_tax_rate2": book_header_sun[12] if book_header_sun[12] > 0 else "",
            "total_tax_rate3": book_header_sun[13] if book_header_sun[13] > 0 else "",
            "total_tax_rate4": book_header_sun[14] if book_header_sun[14] > 0 else "",
            "total_tax_rate5": book_header_sun[15] if book_header_sun[15] > 0 else "",
            "final_total": book_header_sun[3] if book_header_sun[3] > 0 else "",
            "final_total_tax": book_header_sun[4] if book_header_sun[4] > 0 else "",
            "fiscal_total": book_header_sun[5] if book_header_sun[5] > 0 else "",
            "fiscal_total_tax": book_header_sun[6] if book_header_sun[6] > 0 else "",
            "ncfinal_total": book_header_sun[7] if book_header_sun[7] > 0 else "",
            "ncfinal_total_tax": book_header_sun[8] if book_header_sun[8] > 0 else "",
            "ncfiscal_total": book_header_sun[9] if book_header_sun[9] > 0 else "",
            "ncfiscal_total_tax": book_header_sun[10] if book_header_sun[10] > 0 else "",
        }

        return values

    def create_month_book(self,daily_books,month_total_info):
        
        #Se unen todas la lineas de los libros diarios
        daily_info = ""
        mti = month_total_info
        for book in daily_books:
            daily_book_row = base64.b64decode(book.book).decode('utf-8')
            daily_info += daily_book_row
        #Se crea el HASH de la Linea
        hash_string = hashlib.sha1(bytes(daily_info, 'utf-8')).hexdigest().upper()
        
        #Generar la linea del resumen de las ventas
        month_resume_line = "3||"+hash_string+"||"+str(mti['doc_qty'])+"||"+str(mti['total'])\
        +"||"+str(mti['total_tax'])+"||"+str(mti['total_tax_rate1'])+"||"+str(mti['total_tax_rate2'])+"||"+str(mti['total_tax_rate3'])\
        +"||"+str(mti['total_tax_rate4'])+"||"+str(mti['total_tax_rate5'])+"||"+str(mti['final_total'])+"||"+str(mti['final_total_tax'])\
        +"||"+str(mti['fiscal_total'])+"||"+str(mti['fiscal_total_tax'])+"||"+str(mti['ncfinal_total'])+"||"+str(mti['ncfinal_total_tax']) \
        +"||"+str(mti['ncfiscal_total'])+"||"+str(mti['ncfiscal_total_tax'])+"||\n"

    
        month_book =  month_resume_line + daily_info

        return month_book
        

    @api.model
    def save_book(self, new_book, serial, bookday):
        printer_id = self.get_ipf_host(get_id=True)
        date = bookday.split("-")
        printer_config = self.get_user_printer()
        ext = printer_config.extension  if printer_config.extension != "" else "000"
        filename = "LV{}{}{}.{}".format(date[0][2:4], date[1], date[2], ext)

        book = self.env["ipf.daily.book"].search([('printer_id', '=', printer_id), ('date', '=', bookday)])
        if book:
            book.unlink()
        values = {"printer_id": printer_id, "date": bookday, "book": base64.b64encode(new_book.encode("utf-8")), "serial": printer_config.serial,
                  "filename": filename}

        new_book = self.env["ipf.daily.book"].create(values);

        self.set_book_totals(new_book)

        return True

    @api.model
    def generate_month_book(self, year, month):
        printer_id = self.get_user_printer()
        book_monthrange =  calendar.monthrange(int(year), int(month) + 1 )
        str_month = month if int(month) >= 10 else "0"+month
        date_choose =  year+str_month

        first_day_month = datetime.datetime(int(year), int(month) + 1 , book_monthrange[0])
        last_day_month =  datetime.datetime(int(year), int(month) + 1, book_monthrange[1])

        date1 = format_date(self.env, first_day_month, date_format='YYYY-MM-dd')
        date2 = format_date(self.env, last_day_month, date_format='YYYY-MM-dd')

        domain = [('printer_id', '=', printer_id.id)]
        domain.append(('date', '>=', first_day_month))
        domain.append(('date', '<=', last_day_month))
        
        daily_books = self.env["ipf.daily.book"].search(domain,order='date')

        if not daily_books:
            return False

        monthly_info = self.get_books_totals(daily_books)
        month_file = self.create_month_book(daily_books, monthly_info)

        ext = printer_id.extension  if printer_id.extension != "" else "000"
        filename = "LVM{}{}.{}".format(year, str_month,ext)

        book = self.env["ipf.monthly.book"].search([('printer_id', '=', printer_id.id), ('date_choose', '=', date_choose)])
        if book:
            book.unlink()

        values = {"printer_id": printer_id.id, "date_choose": date_choose, "book": base64.b64encode(month_file.encode("utf-8")), "serial": printer_id.serial,
                  "filename": filename, "year":year, "month": format_date(self.env, last_day_month, date_format='MMMM')}

        new_book = self.env["ipf.monthly.book"].create(values);

        del monthly_info["total_tax_rate1"]
        del monthly_info["total_tax_rate2"]
        del monthly_info["total_tax_rate3"]
        del monthly_info["total_tax_rate4"]
        del monthly_info["total_tax_rate5"]

        new_book.write(monthly_info)

        return True

    
    @api.model
    def save_serial_printer(self, serial):
        printer_id = self.get_ipf_host(get_id=True)
        self.browse(printer_id).write({'serial':serial})
        return True


class ipf_daily_book(models.Model):
    _name = "ipf.daily.book"
    _order = "date desc"

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


class ipf_monthly_book(models.Model):
    _name = "ipf.monthly.book"
    _order = "date desc"

    printer_id = fields.Many2one(
        "ipf.printer.config", string="Printer", readonly=True)
    subsidiary = fields.Many2one(
        "", string="Sucursal", related="printer_id.subsidiary")
    
    date = fields.Date(default=fields.Date.today(), string='Fecha de Generacion',readonly=True)
    serial = fields.Char("Serial", readonly=True)
    book = fields.Binary("Libro mensual", readonly=True)
    filename = fields.Char("file name", readonly=True)
    year = fields.Char("Año", readonly=True)
    month = fields.Char("Mes", readonly=True)
    date_choose = fields.Char("Fecha", readonly=True)

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
