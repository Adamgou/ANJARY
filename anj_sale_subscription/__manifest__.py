# -*- coding: utf-8 -*-
{
    "name": "anj_sale_subscription",
    "summary": """
       Help to manage ANJARY sale_subscipriton spec""",
    "author": "Nexources",
    "website": "https://www.nexources.com/",
    "category": "Sales/Subscriptions",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["sale_subscription"],
    # always loaded
    "data": [
        #data
        "data/cron.xml",
        # views
        "security/security.xml",
        "views/sale_subscription_views.xml",

    ],
    "license": "LGPL-3",
}
