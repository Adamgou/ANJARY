# -*- coding: utf-8 -*-
from datetime import date

from odoo import fields, models, api, _
from odoo.tools import float_round, date_utils, convert_file, html2plaintext
from datetime import datetime


# from odoo.exceptions import UserError, Warning
# raise UserError(f"La date d'entrée ")


class Hr_Payslip(models.Model):
    _inherit = "hr.payslip"
    commentaire = fields.Text(string="Commentaire", required=False)

    paid_date = fields.Date(string="Date de paie ", required=False, readonly=True)

    def compute_sheet(self):
        payslips = self.filtered(lambda slip: slip.state in ["draft", "verify"])
        # delete old payslip lines
        payslips.line_ids.unlink()
        for payslip in payslips:
            number = payslip.number or self.env["ir.sequence"].next_by_code(
                "salary.slip"
            )
            lines = [(0, 0, line) for line in payslip._get_payslip_lines()]
            payslip.write(
                {
                    "line_ids": lines,
                    "number": number,
                    "state": "verify",
                    "compute_date": fields.Date.today(),
                }
            )
        self.paid_date = datetime.now()
        self.contract_id._compute_actual_salary()
        return True

    def get_age(self, birth_date, date_bis):
        age = 0
        if birth_date:
            today = date.today()

            if date_bis:
                end_date = date_bis
                age = end_date.year - birth_date.year

            else:
                age = today.year - birth_date.year

        return age

    def get_spent_monthly_hours(self, monthly_hours):
        if monthly_hours:
            spent_hours = round(((52 * monthly_hours) / 12), 2)
            return spent_hours

    def _get_payslip_lines(self):
        self.ensure_one()

        localdict = self.env.context.get("force_payslip_localdict", None)
        if localdict is None:
            localdict = self._get_localdict()

        rules_dict = localdict["rules"].dict
        result_rules_dict = localdict["result_rules"].dict

        blacklisted_rule_ids = self.env.context.get(
            "prevent_payslip_computation_line_ids", []
        )
        result = {}
        for rule in sorted(self.struct_id.rule_ids, key=lambda x: x.sequence):
            if rule.id in blacklisted_rule_ids:
                continue
            localdict.update(
                {
                    "result": None,
                    "result_qty": 1.0,
                    "result_rate": 100,
                    "result_name": False,
                }
            )
            if rule._satisfy_condition(localdict):
                amount, qty, rate = rule._compute_rule(localdict)
                base = rule._compute_base(localdict)
                nombre = rule._compute_nombre(localdict)
                # check if there is already a rule computed with that code
                previous_amount = rule.code in localdict and localdict[rule.code] or 0.0
                # set/overwrite the amount computed for this rule in the localdict
                tot_rule = amount * qty * rate / 100.0
                localdict[rule.code] = tot_rule
                result_rules_dict[rule.code] = {
                    "total": tot_rule,
                    "amount": amount,
                    "quantity": qty,
                }
                rules_dict[rule.code] = rule
                # sum the amount for its salary category
                localdict = rule.category_id._sum_salary_rule_category(
                    localdict, tot_rule - previous_amount
                )
                # Retrieve the line name in the employee's lang
                employee_lang = self.employee_id.sudo().address_home_id.lang
                # This actually has an impact, don't remove this line
                context = {"lang": employee_lang}
                if localdict["result_name"]:
                    rule_name = localdict["result_name"]
                elif rule.code in [
                    "BASIC",
                    "GROSS",
                    "NET",
                    "DEDUCTION",
                    "REIMBURSEMENT",
                ]:  # Generated by default_get (no xmlid)
                    if (
                            rule.code == "BASIC"
                    ):  # Note: Crappy way to code this, but _(foo) is forbidden. Make a method in master to be overridden, using the structure code
                        if rule.name == "Double Holiday Pay":
                            rule_name = _("Double Holiday Pay")
                        if rule.struct_id.name == "CP200: Employees 13th Month":
                            rule_name = _("Prorated end-of-year bonus")
                        else:
                            rule_name = _("Basic Salary")
                    elif rule.code == "GROSS":
                        rule_name = _("Gross")
                    elif rule.code == "DEDUCTION":
                        rule_name = _("Deduction")
                    elif rule.code == "REIMBURSEMENT":
                        rule_name = _("Reimbursement")
                    elif rule.code == "NET":
                        rule_name = _("Net Salary")
                else:
                    rule_name = rule.with_context(lang=employee_lang).name
                # create/overwrite the rule in the temporary results
                result[rule.code] = {
                    "sequence": rule.sequence,
                    "code": rule.code,
                    "name": rule_name,
                    "note": html2plaintext(rule.note),
                    "salary_rule_id": rule.id,
                    "contract_id": localdict["contract"].id,
                    "employee_id": localdict["employee"].id,
                    "amount": amount,
                    "quantity": qty,
                    "rate": rate,
                    "slip_id": self.id,
                    "base": base,
                    "nombre": nombre,
                }

        return result.values()


    @api.model
    def _get_attachment_types(self):
        return {
            'attachment': self.env.ref('hr_payroll.input_attachment_salary'),
            'assignment': self.env.ref('hr_payroll.input_assignment_salary'),
            'child_support': self.env.ref('hr_payroll.input_child_support'),
            'special_advance': self.env.ref('alpha_payslip.input_special_advance'),
            'advance_15th': self.env.ref('alpha_payslip.input_advance_15th'),
        }
