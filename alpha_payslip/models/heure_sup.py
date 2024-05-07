# -*- coding: utf-8 -*-
from ast import Break
from odoo import fields, models, api, _


def exo(s30, s50, x):
    """
    Fonction qui calcul les heures Exonerés
    """
    if x > 8:
        s30 += 8
        s50 += x - 8
    else:
        s30 += x
    return s30, s50


class HrPayslipInheritHeureSup(models.Model):
    _inherit = "hr.payslip"

    nombre_de_semaine = fields.Selection(
        [("quatre", "4"), ("cinq", "5")], string="Nombre de semaine", default="cinq"
    )

    # Liste de touts le collonnes du tableaux
    heure_sup_s1 = fields.Float(string="Heure sup S1", default=0.0)
    heure_sup_s2 = fields.Float(string="Heure sup S2", default=0.0)
    heure_sup_s3 = fields.Float(string="Heure sup S3", default=0.0)
    heure_sup_s4 = fields.Float(string="Heure sup S4", default=0.0)
    heure_sup_s5 = fields.Float(string="Heure sup S5", default=0.0)
    total_heure_sup = fields.Float(
        string="Total heure sup",
        default=0.0,
        compute="_compute_total_heure_sup",
        store=True,
    )

    @api.depends(
        "heure_sup_s1",
        "heure_sup_s2",
        "heure_sup_s3",
        "heure_sup_s4",
        "heure_sup_s5",
        "nombre_de_semaine",
    )
    def _compute_total_heure_sup(self):
        for rec in self:
            res = 0.0
            res += rec.heure_sup_s1
            res += rec.heure_sup_s2
            res += rec.heure_sup_s3
            res += rec.heure_sup_s4
            if rec.nombre_de_semaine == "cinq":
                res += rec.heure_sup_s5
            rec.sudo().write({"total_heure_sup": res})

    heure_nuit_hab_s1 = fields.Float(string="Heure nuit habituelles S1", default=0.0)
    heure_nuit_hab_s2 = fields.Float(string="Heure nuit habituelles S2", default=0.0)
    heure_nuit_hab_s3 = fields.Float(string="Heure nuit habituelles S3", default=0.0)
    heure_nuit_hab_s4 = fields.Float(string="Heure nuit habituelles S4", default=0.0)
    heure_nuit_hab_s5 = fields.Float(string="Heure nuit habituelles S5", default=0.0)
    total_heure_nuit_hab = fields.Float(
        string="Total heure nuit habituelles",
        default=0.0,
        compute="_compute_total_heure_nuit_hab",
        store=True,
    )

    @api.depends(
        "heure_nuit_hab_s1",
        "heure_nuit_hab_s2",
        "heure_nuit_hab_s3",
        "heure_nuit_hab_s4",
        "heure_nuit_hab_s5",
        "nombre_de_semaine",
    )
    def _compute_total_heure_nuit_hab(self):
        for rec in self:
            res = 0.0
            res += rec.heure_nuit_hab_s1
            res += rec.heure_nuit_hab_s2
            res += rec.heure_nuit_hab_s3
            res += rec.heure_nuit_hab_s4
            if rec.nombre_de_semaine == "cinq":
                res += rec.heure_nuit_hab_s5
            rec.sudo().write({"total_heure_nuit_hab": res})

    heure_nuit_occ_s1 = fields.Float(string="Heure nuit occasionnelles S1", default=0.0)
    heure_nuit_occ_s2 = fields.Float(string="Heure nuit occasionnelles S2", default=0.0)
    heure_nuit_occ_s3 = fields.Float(string="Heure nuit occasionnelles S3", default=0.0)
    heure_nuit_occ_s4 = fields.Float(string="Heure nuit occasionnelles S4", default=0.0)
    heure_nuit_occ_s5 = fields.Float(string="Heure nuit occasionnelles S5", default=0.0)
    total_heure_nuit_occ = fields.Float(
        string="Total heure nuit occasionnelles",
        default=0.0,
        compute="_compute_total_heure_nuit_occ",
        store=True,
    )

    @api.depends(
        "heure_nuit_occ_s1",
        "heure_nuit_occ_s2",
        "heure_nuit_occ_s3",
        "heure_nuit_occ_s4",
        "heure_nuit_occ_s5",
        "nombre_de_semaine",
    )
    def _compute_total_heure_nuit_occ(self):
        for rec in self:
            res = 0.0
            res += rec.heure_nuit_occ_s1
            res += rec.heure_nuit_occ_s2
            res += rec.heure_nuit_occ_s3
            res += rec.heure_nuit_occ_s4
            if rec.nombre_de_semaine == "cinq":
                res += rec.heure_nuit_occ_s5
            rec.sudo().write({"total_heure_nuit_occ": res})

    heure_sup_dimanche_s1 = fields.Float(
        string="Heures travaillées le dimanche S1", default=0.0
    )
    heure_sup_dimanche_s2 = fields.Float(
        string="Heures travaillées le dimanche S2", default=0.0
    )
    heure_sup_dimanche_s3 = fields.Float(
        string="Heures travaillées le dimanche S3", default=0.0
    )
    heure_sup_dimanche_s4 = fields.Float(
        string="Heures travaillées le dimanche S4", default=0.0
    )
    heure_sup_dimanche_s5 = fields.Float(
        string="Heures travaillées le dimanche S5", default=0.0
    )
    total_heure_sup_dimanche = fields.Float(
        string="Total heures travaillées le dimanche",
        default=0.0,
        compute="_compute_total_heure_sup_dimanche",
        store=True,
    )

    @api.depends(
        "heure_sup_dimanche_s1",
        "heure_sup_dimanche_s2",
        "heure_sup_dimanche_s3",
        "heure_sup_dimanche_s4",
        "heure_sup_dimanche_s5",
        "nombre_de_semaine",
    )
    def _compute_total_heure_sup_dimanche(self):
        for rec in self:
            res = 0.0
            res += rec.heure_sup_dimanche_s1
            res += rec.heure_sup_dimanche_s2
            res += rec.heure_sup_dimanche_s3
            res += rec.heure_sup_dimanche_s4
            if rec.nombre_de_semaine == "cinq":
                res += rec.heure_sup_dimanche_s5
            rec.sudo().write({"total_heure_sup_dimanche": res})

    heure_sup_ferie_s1 = fields.Float(
        string="Heures travaillées en jour férié S1", default=0.0
    )
    heure_sup_ferie_s2 = fields.Float(
        string="Heures travaillées en jour férié S2", default=0.0
    )
    heure_sup_ferie_s3 = fields.Float(
        string="Heures travaillées en jour férié S3", default=0.0
    )
    heure_sup_ferie_s4 = fields.Float(
        string="Heures travaillées en jour férié S4", default=0.0
    )
    heure_sup_ferie_s5 = fields.Float(
        string="Heures travaillées en jour férié S5", default=0.0
    )
    total_heure_sup_ferie = fields.Float(
        string="Total heures travaillées en jour férié",
        default=0.0,
        compute="_compute_total_heure_sup_ferie",
        store=True,
    )

    @api.depends(
        "heure_sup_ferie_s1",
        "heure_sup_ferie_s2",
        "heure_sup_ferie_s3",
        "heure_sup_ferie_s4",
        "heure_sup_ferie_s5",
        "nombre_de_semaine",
    )
    def _compute_total_heure_sup_ferie(self):
        for rec in self:
            res = 0.0
            res += rec.heure_sup_ferie_s1
            res += rec.heure_sup_ferie_s2
            res += rec.heure_sup_ferie_s3
            res += rec.heure_sup_ferie_s4
            if rec.nombre_de_semaine == "cinq":
                res += rec.heure_sup_ferie_s5
            rec.sudo().write({"total_heure_sup_ferie": res})

    total_s1 = fields.Float(
        string="Total S1", default=0.0, compute="_compute_total_s1", store=True
    )

    @api.depends(
        "heure_sup_s1",
        "heure_sup_dimanche_s1",
        "heure_sup_ferie_s1",
        "heure_nuit_occ_s1",
        "heure_nuit_hab_s1",
    )
    def _compute_total_s1(self):
        for rec in self:
            res = 0.0
            res += rec.heure_sup_s1
            res += rec.heure_sup_dimanche_s1
            res += rec.heure_sup_ferie_s1
            res += rec.heure_nuit_occ_s1
            res += rec.heure_nuit_hab_s1
            rec.sudo().write({"total_s1": res})

    total_s2 = fields.Float(
        string="Total S2", default=0.0, compute="_compute_total_s2", store=True
    )

    @api.depends(
        "heure_sup_s2",
        "heure_sup_dimanche_s2",
        "heure_sup_ferie_s2",
        "heure_nuit_occ_s2",
        "heure_nuit_hab_s2",
    )
    def _compute_total_s2(self):
        for rec in self:
            res = 0.0
            res += rec.heure_sup_s2
            res += rec.heure_sup_dimanche_s2
            res += rec.heure_sup_ferie_s2
            res += rec.heure_nuit_occ_s2
            res += rec.heure_nuit_hab_s2
            rec.sudo().write({"total_s2": res})

    total_s3 = fields.Float(
        string="Total S3", default=0.0, compute="_compute_total_s3", store=True
    )

    @api.depends(
        "heure_sup_s3",
        "heure_sup_dimanche_s3",
        "heure_sup_ferie_s3",
        "heure_nuit_occ_s3",
        "heure_nuit_hab_s3",
    )
    def _compute_total_s3(self):
        for rec in self:
            res = 0.0
            res += rec.heure_sup_s3
            res += rec.heure_sup_dimanche_s3
            res += rec.heure_sup_ferie_s3
            res += rec.heure_nuit_occ_s3
            res += rec.heure_nuit_hab_s3
            rec.sudo().write({"total_s3": res})

    total_s4 = fields.Float(
        string="Total S4", default=0.0, compute="_compute_total_s4", store=True
    )

    @api.depends(
        "heure_sup_s4",
        "heure_sup_dimanche_s4",
        "heure_sup_ferie_s4",
        "heure_nuit_occ_s4",
        "heure_nuit_hab_s4",
    )
    def _compute_total_s4(self):
        for rec in self:
            res = 0.0
            res += rec.heure_sup_s4
            res += rec.heure_sup_dimanche_s4
            res += rec.heure_sup_ferie_s4
            res += rec.heure_nuit_occ_s4
            res += rec.heure_nuit_hab_s4
            rec.sudo().write({"total_s4": res})

    total_s5 = fields.Float(
        string="Total S5", default=0.0, compute="_compute_total_s5", store=True
    )

    @api.depends(
        "heure_sup_s5",
        "heure_sup_dimanche_s5",
        "heure_sup_ferie_s5",
        "heure_nuit_occ_s5",
        "heure_nuit_hab_s5",
    )
    def _compute_total_s5(self):
        for rec in self:
            res = 0.0
            res += rec.heure_sup_s5
            res += rec.heure_sup_dimanche_s5
            res += rec.heure_sup_ferie_s5
            res += rec.heure_nuit_occ_s5
            res += rec.heure_nuit_hab_s5
            rec.sudo().write({"total_s5": res})

    def calcul_cell(self):
        """
        Un bouton qui va ajouter les heures supplémentaaire dans la section autre types d'heures
        après les avoir calculer.
        """
        self.ensure_one()
        for line in self.input_line_ids:
            if line.input_type_id.generate:
                self.input_line_ids = [(2, line.id)]

        self.input_line_ids = [
            (
                0,
                0,
                {
                    "input_type_id": self.env.ref("alpha_payslip.heure_sup").id,
                    "amount": self.total_heure_sup,
                },
            )
        ]

        self.input_line_ids = [
            (
                0,
                0,
                {
                    "input_type_id": self.env.ref(
                        "alpha_payslip.heure_sup_nuit_hab"
                    ).id,
                    "amount": self.total_heure_nuit_hab,
                },
            )
        ]

        self.input_line_ids = [
            (
                0,
                0,
                {
                    "input_type_id": self.env.ref(
                        "alpha_payslip.heure_sup_nuit_occ"
                    ).id,
                    "amount": self.total_heure_nuit_occ,
                },
            )
        ]

        self.input_line_ids = [
            (
                0,
                0,
                {
                    "input_type_id": self.env.ref("alpha_payslip.heure_sup_dim").id,
                    "amount": self.total_heure_sup_dimanche,
                },
            )
        ]

        self.input_line_ids = [
            (
                0,
                0,
                {
                    "input_type_id": self.env.ref("alpha_payslip.heure_sup_fer").id,
                    "amount": self.total_heure_sup_ferie,
                },
            )
        ]

        only_hsup30, only_hsup50 = 0, 0
        only_hsup30, only_hsup50 = exo(only_hsup30, only_hsup50, self.heure_sup_s1)
        only_hsup30, only_hsup50 = exo(only_hsup30, only_hsup50, self.heure_sup_s2)
        only_hsup30, only_hsup50 = exo(only_hsup30, only_hsup50, self.heure_sup_s3)
        only_hsup30, only_hsup50 = exo(only_hsup30, only_hsup50, self.heure_sup_s4)
        if self.nombre_de_semaine == "cinq":
            only_hsup30, only_hsup50 = exo(only_hsup30, only_hsup50, self.heure_sup_s5)
        self.input_line_ids = [
            (
                0,
                0,
                {
                    "input_type_id": self.env.ref("alpha_payslip.heure_sup_30").id,
                    "amount": only_hsup30,
                },
            )
        ]

        self.input_line_ids = [
            (
                0,
                0,
                {
                    "input_type_id": self.env.ref("alpha_payslip.heure_sup_50").id,
                    "amount": only_hsup50,
                },
            )
        ]

        hsup30, hsup50, hsup30_old, hsup50_old, res1, res2 = 0, 0, 0, 0, 0, 0
        for index, total in enumerate(
                [
                    self.total_s1,
                    self.total_s2,
                    self.total_s3,
                    self.total_s4,
                    self.total_s5,
                ]
        ):
            res1, res2 = hsup30, hsup50
            if hsup30 + hsup50 > 20:
                a = 20 - hsup30
                if a < 0:
                    res1 = 20 - hsup50_old
                    res2 = hsup50_old
                else:
                    res1 = hsup30
                    res2 = 20 - res1
                break
            else:
                x, y = exo(0, 0, total)
                if hsup30 + hsup50 + x > 20:
                    res1 = 20 - hsup50
                    res2 = hsup50
                    break

            hsup30_old, hsup50_old = hsup30, hsup50
            if index == 4:
                if self.nombre_de_semaine == "cinq":
                    hsup30, hsup50 = exo(hsup30, hsup50, total)
            else:
                hsup30, hsup50 = exo(hsup30, hsup50, total)
        self.input_line_ids = [
            (
                0,
                0,
                {
                    "input_type_id": self.env.ref("alpha_payslip.heure_sup_non_30").id,
                    "amount": res1,
                },
            )
        ]

        self.input_line_ids = [
            (
                0,
                0,
                {
                    "input_type_id": self.env.ref("alpha_payslip.heure_sup_non_50").id,
                    "amount": res2,
                },
            )
        ]
        message = _("Les heures supplémmentaires ont été calculées avec succès")
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "message": message,
                "type": "success",
                "sticky": False,
                "next": {"type": "ir.actions.act_window_close"},
            },
        }
