# -*- coding: utf-8 -*-
{
    'name': "Almacen solo lectura por defecto",
    'summary': """
        Este modulo agrega campo de almacen en el modulo de usuarios
    """,
    'description': """
        Este modulo permite asignar un almacen por defecto al usuario y no permite que el usuario modifique el almacen de facturacion al momento de hacer el pedido de venta
    """,
    'author': "Anthony Martinez - (anthonyame02@gmail.com)",
    'website': "",
    'data': [
        'views/users_stock_view.xml',
        'views/sale_order_stock_readonly_view.xml',
    ],
    'category': 'Hidden',
    'version': '12.0',
    'depends': ['base', 'stock', 'sale'],
    'images': '',
}
