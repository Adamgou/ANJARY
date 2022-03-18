# -*- coding: utf-8 -*-
{
    'name': "anj_location",

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
    'depends': ['base','anj_base','sale_renting','stock','mail','sale_renting'],

    # always loaded
    'data': [
        'views/views.xml',
        'views/templates.xml',
        'views/location_price.xml',
        'views/product_template.xml',
        'views/rental_wizard.xml',
        'views/sale_renting.xml',
        'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}