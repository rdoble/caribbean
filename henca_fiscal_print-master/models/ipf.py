# -*- coding: utf-8 -*-


from odoo import models, fields


class ipf_printer_config(models.Model):
    _name = 'ipf.printer.config'

    name = fields.Char("Descripcion", required=True)
    host = fields.Char("Host", required=True)

    user_ids = fields.Many2many('res.users', string="Usuarios", required=True)

    print_copy = fields.Boolean("Imprimir con copia", default=False)
    subsidiary = fields.Many2one("shop.ncf.config", string="Sucursal", required=False)

    active = fields.Boolean(default=True)
    
    serial = fields.Char("Serial de la impresora", readonly=True)

    def toggle_active(self):
        self.active = not self.active
    
    def z_close_print(self):
        pass

    