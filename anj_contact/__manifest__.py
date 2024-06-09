# -*- coding: utf-8 -*-
{
    'name': "anj_contact",

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
    'depends': ['contacts', 'anj_base', 'base_vat', 'hr', 'stock'],

    # always loaded
    'data': [
        # 'data/res_city_data.xml',
        'security/ir.model.access.csv',
        'views/partner.xml',
        'views/contact_views.xml',
    ],

'license': 'LGPL-3',
}
