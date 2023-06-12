from odoo import models
from datetime import date


def add_zeros(str_value, length):
    zeros_to_add = length - len(str_value)
    str_value = '0' * zeros_to_add + str_value
    return str_value


def float_to_string(float_num):
    num_str = str(float_num)
    num_str = num_str.replace('.', '')
    return num_str


class HrPayslipXlsx(models.AbstractModel):
    _name = 'report.opavie_excel_report.report_opavie_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        employer_bank_account = add_zeros(lines.employer_bank_account.acc_number.replace(' ', ''), 23) if lines.employer_bank_account.acc_number else " "
        report_name = 'Salaire' + ' ' + lines.date_start.strftime("%m%y")
        total = 0
        for value in lines.slip_ids:
            total = total + value.basic_wage
        sheet = workbook.add_worksheet('OPAVI report')
        sheet.write(0, 0, employer_bank_account)
        sheet.write(0, 1, add_zeros(str(total).replace('.', ''), 12))
        # sheet.write(0, 2, '')
        sheet.write(0, 3, report_name)
        for index, value in enumerate(lines.slip_ids):
            employee_bank_account = add_zeros(value.employee_id.bank_account_id.acc_number.replace(' ', ''),
                                              23) if value.employee_id.bank_account_id.acc_number else " "
            employee_salary = add_zeros(str(value.basic_wage).replace('.', ''), 12)
            employee_matricule = value.employee_id.matricule if value.employee_id.matricule else " "
            employee_name = value.employee_id.name if value.employee_id.name else " "
            sheet.write(index + 1, 0, employee_bank_account)
            sheet.write(index + 1, 1, employee_salary)
            sheet.write(index + 1, 2, employee_matricule)
            sheet.write(index + 1, 3, employee_name)
