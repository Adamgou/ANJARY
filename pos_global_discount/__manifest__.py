# coding: utf-8
{
    "name": "POS GLOBAL DISCOUNT",
    "author": "nexources",
    "version": "17.0",
    "summary": "Simple Discounts in the Point of Sale ",
    "website": "http://www.nexources.com",
    "category": "Sales/Point of Sale",
    "depends": ["pos_discount", "anj_base"],
    "data": [
        "views/pos_config_views.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_global_discount/static/src/**/*",
        ],
    },
    "license": "LGPL-3",
}
