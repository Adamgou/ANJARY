from odoo import models, fields


class ResUsers(models.Model):
    """Extend res.users to manage specific needs"""

    _inherit = "res.users"

    pos_config_id = fields.Many2one(comodel_name="pos.config")
