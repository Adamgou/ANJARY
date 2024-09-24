# -*- coding: utf-8 -*-
{
    "name": "ANJARY - BISKO",
    "author": "Nexources",
    "website": "https://www.nexources.com",
    "category": "spoo/poin of sale",
    "version": "0.1",
    "depends": ["account", "anj_contact", "point_of_sale", "anj_sale"],
    "data": [
        # data
        "data/report_paperformat_data.xml",
        # 'security/ir.model.access.csv',
        # views
        "views/product_template_inherit_views.xml",
        "views/res_company_views.xml",
        # report
        "report/point_of_sale_report.xml",
        "report/report_inherit_saledetails.xml",
        "report/report_sale_detailss_inherit.xml",
    ],
    "license": "LGPL-3",
}
