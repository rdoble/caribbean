# -*- coding: utf-8 -*-

{
    'name': "Henca Fiscal Print",

    'summary': """
        Controlador para impresoras fiscales EPSON TM-T88v.
    """,

    'description': """
        Este modulo permite que odoo pueda imprimir desde el facturacion 
        en la impresora fiscal EPSON TM-T88v utilizando una interface fiscal.
    """,

    'author': "Grupo Consultoria Henca ",
    'category': 'Uncategorized',
    'version': '12.0',
    'depends': ['base', 'web', 'account', 'ncf_manager'],
    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/ipf_view.xml',
        'views/account_invoice_view.xml',

    ],
    'license': "Other proprietary"
}
