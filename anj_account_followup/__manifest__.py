# -*- coding: utf-8 -*-
{
    "name": "anj_account_followup",
    "author": "My Company",
    "website": "http://www.yourcompany.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Uncategorized",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["base", "account_followup"],
    # always loaded
    "data": [
        "views/report_followup.xml",
    ],

    "license": "LGPL-3",
}
