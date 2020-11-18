# -*- coding: utf-8 -*-
{
    'name': "Fiscal Henca Solo Facturacion",

    'summary': """
      
       Controlador para impresoras fiscales.
        
        Este modulo permite que odoo pueda imprimir desde facturacion

        en la impresora fiscal EPSON TM-T88v y Bixolon utilizando una interfaz fiscal

        """,

    'description': """
         Controlador para impresoras fiscales.
    """,
    'author': "Grupo Consultoria Henca, Jorge Miguel Hernandez Santos(dev.jhernandez@gmail.com)",
    'category': 'Fiscal',
    'version': '13.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'account', 'l10n_do_accounting'],

    # always loaded
     'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/ipf_view.xml',
        'views/account_invoice_view.xml',

    ]
}
