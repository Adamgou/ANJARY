# -*- coding: utf-8 -*-
{
    'name': "anj_stock",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','anj_base', 'product', 'stock'],

    # always loaded
    'data': [
        #security
        # 'security/ir.model.access.csv',
        'security/res_groups.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/product_template_view.xml',
        'views/stock_quant_views.xml',
        # report
        'report/report_delivery.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'stock.assets': [
            'anj_stock/static/src/css/report_bl.css',
        ],
    },
    'license': 'LGPL-3',
    "uninstall_hook": "uninstall_hook",
}
