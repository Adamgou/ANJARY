# coding: utf-8
{
    "name": "ANJARY - STOCK",
    "author": "nexources",
    "website": "http://www.nexources.com",
    "category": "Inventory/Inventory",
    "version": "17.1",
    # any module necessary for this one to work correctly
    "depends": ["stock", "anj_base"],
    # always loaded
    "data": [
        # security
        "security/res_groups.xml",
        "views/product_template_views.xml",
        "views/stock_quant_views.xml",
        # report
        "report/report_delivery.xml",
    ],
    "assets": {
        "stock.assets": [
            "anj_stock/static/src/css/report_bl.css",
        ],
    },
    "license": "LGPL-3",
    "uninstall_hook": "uninstall_hook",
}
