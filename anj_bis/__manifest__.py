# -*- coding: utf-8 -*-
{
    "name": "ANJARY - BISKO",
    "author": "Nexources",
    "website": "https://www.nexources.com",
    "category": "spoo/poin of sale",
    "version": "0.1",
    "depends": ["account", "anj_contact", "point_of_sale", "anj_sale"],
    "data": [
        # 'security/ir.model.access.csv',
        "views/pos_config_views.xml",
        "views/res_config_settings_views.xml",
        "views/product_template_inherit_views.xml",
        "views/res_company_views.xml",
        "report/report_inherit_saledetails.xml",
        "report/report_sale_detailss_inherit.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "anj_bis/static/src/app/**/*",
        ]
    },
    "license": "LGPL-3",
}
