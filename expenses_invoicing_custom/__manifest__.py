# -*- coding: utf-8 -*-
{
    'name': "Creación de factura a través de gastos",
    'summary': """Funcionalidad de creación de facturas de proveedor a través del módulo de gastos para su visualización en los reportes fiscales.""",
    'author': "José Romero",
    'category': 'Invoicing',
    'version': '12.0.1',
    'depends': [
        'base',
        'account',
        'hr_expense',
        'ncf_manager',
    ],
    'data': [
        'views/hr_expense_views.xml',
        'views/account_invoice_views.xml',
    ],
}
