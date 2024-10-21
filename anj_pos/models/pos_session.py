# coding: utf-8

from odoo import models, _
import base64


class PosSession(models.Model):
    _inherit = "pos.session"

    def close_session_from_ui(self, bank_payment_method_diff_pairs=None):
        out = super(PosSession, self).close_session_from_ui(
            bank_payment_method_diff_pairs
        )
        if self.env.company.is_biskot:
            pdf = (
                self.env["ir.actions.report"]
                .sudo()
                ._render_qweb_pdf("point_of_sale.sale_details_report", [self.id])
            )
            email_to_list = [
                "adam@anjarygroup.com",
                "diary@anjarygroup.com",
                "cafespoon.direction@gmail.com",
            ]
            mail_values = {
                "subject": _("Sales Details Report"),
                "body_html": _("Please find attached the sales details report."),
                "email_to": ",".join(email_to_list),
                "auto_delete": False,
                "email_cc": "mahery@nexources.com",
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

            mail = self.env["mail.mail"].sudo().create(mail_values)
            mail.send()
        return out
