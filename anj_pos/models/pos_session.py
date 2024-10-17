# coding: utf-8

from odoo import models, _
import base64


class PosSession(models.Model):
    _inherit = "pos.session"

    def close_session_from_ui(self, bank_payment_method_diff_pairs=None):
        out = super(PosSession, self).close_session_from_ui(
            bank_payment_method_diff_pairs
        )
        if self.env.company.name.lower() == "biskot":
            pdf = self.env['ir.actions.report'].sudo()._render_qweb_pdf("point_of_sale.sale_details_report", [self.id])
            mail_values = {
                "subject": _("Sales Details Report"),
                "body_html": _("Please find attached the sales details report."),
                "email_to": "adam@anjarygroup.com",
                'partner_ids': [42],
                "email_cc": "diary@anjarygroup.com",
                "attachment_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Salesdetails_report.pdf",
                            "type": "binary",
                            "datas": base64.b64encode(pdf[0]),
                            "mimetype": "application/pdf",
                        },
                    )
                ],
            }

            mail = self.env["mail.mail"].create(mail_values)
            mail.send()
        return out
