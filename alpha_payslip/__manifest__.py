# -*- coding: utf-8 -*-
{
    "name": "alpha_payslip",
    "summary": """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
    "description": """
        Long description of module's purpose
    """,
    "author": "My Company",
    "website": "http://www.yourcompany.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Uncategorized",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["base", "hr_contract", "hr_work_entry", "hr", "hr_payroll"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/base_external_layout.xml",
        "views/views.xml",
        "views/templates.xml",
        "views/hr_employee.xml",
        "views/hr_contract_view.xml",
        "views/payslip_report.xml",
        "views/hr_payslip.xml",
        "views/heure_sup.xml",
        "views/hr_contract_view_too.xml",
        "views/hr_salary_rule_views.xml",
        "views/hr_work_entry.xml",
        "views/company.xml",
        "data/data.xml",
    ],
    "license": "LGPL-3",
    "assets": {
        "web.report_assets_common": [
            "alpha_payslip/static/src/css/bootstrap.css",
        ],
        "web.assets_backend": [
            "alpha_payslip/static/src/css/custom_widget.css",
            "alpha_payslip/static/src/js/custom_widget.js",
        ],
        "web.assets_qweb": {
            "alpha_payslip/static/src/xml/custom_widget.xml",
        },
    },
}
