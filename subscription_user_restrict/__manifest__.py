# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Subscription user restrict',
    'version' : '1.1',
    'summary': 'Restrict subscription access for certain users',
    'sequence': 10,
    'category': 'Subscription/Subscription',
    'website': 'https://www.nexources.com',
    'depends' : ['sale_subscription'],
    'data': [
        'security/ir_rule.xml',
        'views/sale_subscription_views.xml'
    ],
    'license': 'LGPL-3',
}
