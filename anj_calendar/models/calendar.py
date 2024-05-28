# coding: utf-8

from odoo import models, fields, api


class Calendar(models.Model):
    _inherit = "calendar.event"

    @api.model
    def get_alarm(self):
        return [
            fields.Command.set(
                self.env["calendar.alarm"].search([("is_default", "=", True)]).ids
            )
        ]

    alarm_ids = fields.Many2many(default=get_alarm)
    privacy = fields.Selection(default="private")


class CalendarAlarm(models.Model):
    _inherit = "calendar.alarm"

    is_default = fields.Boolean(f"Rappel d'alarme par défault")
