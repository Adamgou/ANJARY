# -*- coding: utf-8 -*-

{
    'name': 'ANJARY - Inter Company Module for Sale/Purchase Orders and Invoices and Pickings',
    'version': '15.0.0.1',
    'category': 'Productivity',
    'summary': 'Intercompany SO/PO/INV/SP rules',
    'description': """
        Module for synchronization of Documents between several companies. For example, this allow you to have a Sales Order created automatically when a Purchase Order is validated with another company of the system as vendor, and inversely.

        Supported documents are SO, PO.
    """,
    'author': "Nexources",
    'license': "LGPL-3",
    'depends': [
        'sale_purchase_inter_company_rules',
    ],
    'data': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
