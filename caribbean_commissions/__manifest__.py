# -*- coding: utf-8 -*-
{
    'name': "Parametrización de comisiones",
    'summary': """
        Parametrización de comisiones para la generación de reportes de ventas
    """,
    'description': """
        Modulo para parametrizar y configurar las comisiones que se utilizan los de reportes de ventas
    """,
    'author': "Anthony Martinez - (anthonyame02@gmail.com)",
    'website': "",
    'category': 'Sales',
    'version': '12.0',
    'depends': ['base', 'web', 'hr', 'caribbean_reports'],
    'data': [
        'views/caribbean_sales_commission_setting_view.xml',
        'views/caribbean_sales_commission_equipment_margin_view.xml',
        'views/caribbean_sales_commission_setting_menu.xml',
        'views/caribbean_hr_employee_commissions_view.xml',
        'security/caribbean_reports_security.xml',
        'security/ir.model.access.csv',
    ],
    'images': '',
}
