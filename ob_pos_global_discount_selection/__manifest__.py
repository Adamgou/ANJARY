# -*- coding: utf-8 -*-
######################################################################################
#
#    Odoo Being
#
#    Copyright (C) 2021-TODAY Odoo Being(<https://www.odoobeing.com>).
#    Author: Odoo Being(<https://www.odoobeing.com>)
#
#    This program is under the terms of the Odoo Proprietary License v1.0 (OPL-1)
#    It is forbidden to publish, distribute, sublicense, or sell copies of the Software
#    or modified copies of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#    DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#    ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#    DEALINGS IN THE SOFTWARE.
#
########################################################################################
{
    "name": "POS Global Discount in Amount",

    "summary": """Apply discount amount instead of percentage for global discount in POS""",

    "description": """
        Apply discount amount instead of percentage for global discount in POS
    """,

    "author": "Odoo Being",
    "website": "https://odoobeing.com",
    "license": "OPL-1",
    "category": "Point of Sale",
    "version": "15.0.1.0.1",
    "depends": ["pos_discount"],
    "support": "odoobeing@gmail.com",
    "currency": "USD",
    "price": "10",
    "installable": True,
    "auto_install": False,
    "data": [
        "views/pos_config.xml",
    ],
    'assets': {
        'point_of_sale.assets': [
            '/ob_pos_global_discount_selection/static/src/js/DiscountButton.js',
        ],
    },
    'images': ['static/description/images/pos_global_discount_amount_percentage.png'],
}
