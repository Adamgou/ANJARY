{
    "name": "ANJARY - SECURITY",
    "version": "17.0.1.0.0",
    "website": "http://www.nexources.com",
    "license": "AGPL-3",
    "data": [
        "views/res_users_views.xml",
        "views/pos_config_views.xml",
        "security/ir_rule.xml",
    ],
    "depends": ["anj_pos", "pos_hr"],
    "assets": {
        "point_of_sale._assets_pos": [
            "anj_security/static/src/app/store/pos_store.js",
            "anj_security/static/src/navbar/navbar.xml",
        ],
    },
}
