from odoo import models, fields, api


class ResUsers(models.Model):
    """Extend res.users to manage specific needs"""

    _inherit = "res.users"

    pos_config_id = fields.Many2one(comodel_name="pos.config")
    no_backend_access = fields.Boolean(compute="_compute_no_backend_access", store=True)

    @api.depends("pos_config_id")
    def _compute_no_backend_access(self):
        """Users with defined pos_config_id should not have access to the backend"""
        for user in self:
            user.no_backend_access = bool(user.pos_config_id)
