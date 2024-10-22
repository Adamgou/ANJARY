# coding: utf-8
{
    "name": "ANJARY - POS",
    "author": "nexources",
    "website": "http://www.nexources.com",
    "category": "Sales/Point of Sale", 
    "version": "17.1",
    "depends": ["point_of_sale", "anj_base", "account", "anj_bis"],
    "data": [
        "views/product_template_form_view_inherit.xml",
        "views/pos_config_view_form_inherit.xml",
    ],
    "license": "LGPL-3",
    "assets": {
        "point_of_sale._assets_pos": [
            "anj_pos/static/src/app/**/*",
        ]
    },
}
