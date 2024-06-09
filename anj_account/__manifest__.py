# coding: utf-8
{
    'name': "ANJARY - ACCOUNT",

    'author': "nexources",
    'website': "http://www.nexources.com",

    'category': 'Accounting/Accounting',
    'version': '17.0',

    'depends': ['anj_contact', 'account'],

    'data': [
        'security/res_group.xml',
        # views
        'views/res_partner_views.xml',
        'views/account_move_views.xml',
        'views/account_payment_view.xml',
        'views/journal_account_views.xml',
        'views/account_move.xml',
        'views/product_template.xml',
        'report/report_invoice.xml',
    ],
    'license': 'LGPL-3',
}
