# -*- coding: utf-8 -*-


from odoo import models, fields


class ipf_printer_config(models.Model):
    _name = 'ipf.printer.config'

    name = fields.Char(
        string="Descripcion",
        required=True
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

    def toggle_active(self):
        self.active = not self.active
    
    def z_close_print(self):
        pass

    