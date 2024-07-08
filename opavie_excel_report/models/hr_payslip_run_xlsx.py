from odoo import models, _
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
        employer_bank_account = add_zeros(lines.employer_bank_account.acc_number.replace(' ', ''),
                                          23) if lines.employer_bank_account.acc_number else " "
        report_name = 'Salaire' + ' ' + lines.date_start.strftime("%m%y")
        title_style = workbook.add_format({'font_name': 'Arial', 'bold': True, 'font_size': 16,'align': 'center','bg_color': '#FF9999'})
        title_body = workbook.add_format({'align': 'center','border': 1})
        total = 0
        total_net = 0
        for value in lines.slip_ids:
            net_salary = value.line_ids.filtered(lambda payslip: payslip.salary_rule_id.is_net)[0].total if \
            value.line_ids.filtered(lambda payslip: payslip.salary_rule_id.is_net)[0].total else 0
            total = total + net_salary
        total_net = add_zeros(str(total).replace('.', ''), 12)
        sheet = workbook.add_worksheet('OPAVI report')
        sheet.set_column(0, 0, 10)
        sheet.set_column(0, 1, 43)
        sheet.set_column(0, 2, 43)
        sheet.set_column(0, 3, 43)

        if self.env.company.name.lower().startswith('jara distribution'):
            sheet.write(0, 0, _('00005000067069530000113'),title_body)
            sheet.write(0, 1, _(total_net),title_body)
            sheet.write(0, 2, _('V00612'),title_body)
            sheet.write(0, 3, _(report_name),title_body)
        elif self.env.company.name.lower().startswith('societe de gestion'):
            sheet.write(0, 0, _('00005000067076067000154'),title_body)
            sheet.write(0, 1, _(total_net),title_body)
            sheet.write(0, 2, _('V00611'),title_body)
            sheet.write(0, 3, _(report_name),title_body)
        elif self.env.company.name.lower().startswith('biskot'):
            sheet.write(0, 0, _('00005000067251439000165'),title_body)
            sheet.write(0, 1, _(total_net),title_body)
            sheet.write(0, 2, _('V00721'),title_body)
            sheet.write(0, 3, _(report_name),title_body)
        for index, value in enumerate(lines.slip_ids):
            employee_bank_account = add_zeros(value.employee_id.bank_account_id.acc_number.replace(' ', ''),
                                              23) if value.employee_id.bank_account_id.acc_number else " "
            employee_salary = add_zeros(
                str(f"{value.line_ids.filtered(lambda payslip: payslip.salary_rule_id.is_net)[0].total:.2f}").replace('.', ''),
                12) if \
                value.line_ids.filtered(lambda payslip: payslip.salary_rule_id.is_net)[0].total else "0"
            employee_matricule = value.employee_id.matricule if value.employee_id.matricule else " "
            employee_function = value.employee_id.job_title if value.employee_id.job_title else " "
            employee_name = value.employee_id.name if value.employee_id.name else " "
            sheet.write(index + 1, 0, employee_bank_account,title_body)
            sheet.write(index + 1, 1, employee_salary,title_body)
            sheet.write(index + 1, 2, employee_matricule,title_body)
            sheet.write(index + 1, 3, employee_name,title_body)
