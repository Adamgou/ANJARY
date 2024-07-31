# coding: utf-8
{
    "name": "ANJARY - PAYROLL",
    "author": "nexources",
    "website": "http://www.nexources.com",
    "category": "Uncategorized",
    "version": "17.1",
    "depends": ["alpha_payslip", "anj_base"],
    "data": [
        # SECURITY
        "security/ir.model.access.csv",
        # VIEWS
        "views/menuitems.xml",
        "views/hr_payslip_views.xml",
        "views/hr_leave_type_views.xml",
        # REPORT
        "report/payslip_report.xml",
    ],
    "license": "LGPL-3",
}
