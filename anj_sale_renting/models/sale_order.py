# coding: utf-8

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    car_registration_ids = fields.Many2many(
        compute="_compute_car_registration_ids", store=True
    )

    @api.depends("order_line.selected_lot_ids")
    def _compute_car_registration_ids(self):
        for rec in self:
            rec.car_registration_ids = [
                (6, 0, rec.order_line.mapped("selected_lot_ids").ids)
            ]

    is_transfert = fields.Boolean("Transfert")

    hotel_partner = fields.Char(
        string="Hotel partenaire", default="Anjary Hotel", required=False
    )

    transfert_date = fields.Date(string="Date de transfert", required=False)

    fligth_company = fields.Char(string="Companie aériène", required=False)

    car_registration_ids = fields.Many2many(
        comodel_name="stock.lot", string="Plaque véhicule"
    )

    employee_id = fields.Many2one("hr.employee", string="Conducteur")

    passenger_list_ids = fields.One2many(
        "passenger.list.praxi", "passenger_sale_order_id", string="Liste de passager"
    )
    passenger_additive_list_ids = fields.One2many(
        "passenger.list.additive",
        "passenger_additive_sale_order_id",
        string="Liste additive des passagers",
    )
    is_additive_passenger = fields.Boolean("Liste additive")
    sale_order_id = fields.Many2one("sale.order", string="Sale Order")

    signatory_name = fields.Char()
    signatory_fonction = fields.Char()
    signatory_phone = fields.Char()

    def action_sms(self):
        date = self.date_order.strftime("%d/%m/%Y")
        driver = self.employee_id.name or ""
        registration_car = self.car_registration or ""

        template_sms = f"""Bonjour {self.partner_id.name}. Votre commande a été confirmée pour le {date}. Véhicule {registration_car}. Chauffeur : {driver}. Praxi vous remercie pour votre confiance."""

        ctx = self._context.copy()

        print(ctx)
        if self.partner_id.mobile:
            tel_phone = self.partner_id.mobile
        elif self.partner_id.phone:
            tel_phone = self.partner_id.phone

        ctx.update(
            {
                "default_recipient_single_number_itf": tel_phone,
                "default_body": template_sms,
            }
        )

        return {
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "sms.composer",
            "target": "new",
            "context": ctx,
        }
