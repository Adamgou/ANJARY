# -*- coding: utf-8 -*-
{
    "name": "anj_sale_renting",
    "summary": """
       Help to manage ANJARY renting spec""",
    "author": "Nexources",
    "website": "https://www.nexources.com/",
    "category": "Sales/Sales",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["anj_location"],
    # always loaded
    "data": [
        'data/location_price.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'anj_sale_renting/static/src/**/*',
        ],
    },
    "license": "LGPL-3",
}
