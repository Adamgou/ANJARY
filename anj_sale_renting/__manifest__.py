# coding: utf-8
{
    "name": "ANJARY - SALE RENTING",
    "summary": """
       Help to manage ANJARY renting spec""",
    "author": "Nexources",
    "website": "https://www.nexources.com/",
    "category": "Sales/Sales",
    "version": "0.1",
    "depends": ["sale_renting"],
    "data": [
        # SECURITY
        "security/ir.model.access.csv",
        # VIEWS
        "views/sale_order_views.xml",
        "views/location_price_views.xml",
        "views/passenger_list_views.xml",
        "wizard/rental_configurator_views.xml",
        # DATA
        "data/location_price.xml",
        # REPORT
        "report/report_transfert_order.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "anj_sale_renting/static/src/js/rental_configurator_model.js",
            "anj_sale_renting/static/src/js/sale_product_field.js",
        ],
    },
    "license": "LGPL-3",
}
