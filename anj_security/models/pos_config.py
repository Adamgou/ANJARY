from odoo import models, fields


class PosConfig(models.Model):
    """Manage some security stuffs"""

    _inherit = "pos.config"

    unauthorized_user_ids = fields.Many2many(comodel_name="res.users")
