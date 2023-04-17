# -*- coding: utf-8 -*-
{
    'name': "anj_account",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.nexources.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','anj_base', 'anj_contact', 'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # views
        'views/views.xml',
        'views/templates.xml',
        'views/res_partner_views.xml',
        'views/account_move_views.xml',
        'views/journal_account_views.xml',
        'views/account_move.xml',
        'views/product_template.xml',
        'report/report_invoice.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    # 'assets': {
    #     'account.assets': [
    #         'anj_account/static/src/css/report_accnt_jd.css',
    #     ],
    #
    # },
    'license': 'LGPL-3',
}
