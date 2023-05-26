# -*- coding: utf-8 -*-

from odoo import fields, models, api
from datetime import date, datetime


class HrContractInherit(models.Model):
    _inherit = "hr.contract"

    @api.depends('base_salary', 'hour_per_week')
    def _compute_hourly_salary(self):
        for rec in self:
            if rec.hour_per_week:
                rec.hourly_salary = rec.base_salary / (rec.hour_per_week * 4)
            else:
                rec.hourly_salary = 0

    contrat_categorie = fields.Selection(
        [('cdi', 'CDI'),
         ('cdd', 'CDD'),
         ('stagiaire', 'Stagiaire'),
         ('temporaire', 'Temporaire')
         ], string='Categorie de contrat', default="cdi",
        required=True, )
    hour_per_week = fields.Float(
        string="Nombre d'heures travaillé par semaine", related="resource_calendar_id.full_time_required_hours",
        required=True)
    base_salary = fields.Monetary('Salaire de base', store=True)
    hourly_salary = fields.Monetary('Salaire horaire', compute='_compute_hourly_salary')
    month_12_last_salary = fields.Monetary('Salaire moyen des 12 derniers mois')
    # production_bonus_participant = fields.Monetary('Prime de production participant')
    allow_transport = fields.Monetary('Indemnité de transport')
    allow_family = fields.Monetary('Allocations familiales')
    allow_logement = fields.Monetary('Indemnité de logement')
    other_allow = fields.Monetary('Autres ndemnités')
    wage = fields.Monetary('Wage', required=True, tracking=True, help="Employee's monthly gross wage.",
                           compute='_compute_base_salary')
    seniority_percentage = fields.Float(string="Pourcentage d'ancienneté", tracking=True, compute='_compute_seniority_percentage', store=True)
    actual_salary = fields.Float('Salaire actuel', tracking=True, compute='_compute_actual_salary')
    seniority = fields.Float('Ancienneté en année', tracking=True, compute='_compute_seniority')

    @api.onchange('date_start')
    def _compute_seniority(self):
        for record in self:
            if record.date_start:
                start_date = record.date_start
                current_date = datetime.now().date()
                year_difference = current_date.year - record.date_start.year
                if current_date.month < start_date.month or (
                        current_date.month == start_date.month and current_date.day <= start_date.day):
                    year_difference -= 1
                record.seniority = year_difference

    @api.onchange('seniority',)
    def _compute_seniority_percentage(self):
        for rec in self:
            num_increases = int(rec.seniority // 3)
            percentage = 0
            for i in range(num_increases):
                percentage += 5
            rec.seniority_percentage = percentage

    @api.depends('seniority_percentage', 'base_salary')
    def _compute_actual_salary(self):
        for rec in self:
            rec.actual_salary = rec.base_salary * (1 + rec.seniority_percentage / 100)

    def _compute_base_salary(self):
        for record in self:
            record.wage = record.base_salary
