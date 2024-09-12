from odoo import models


class PosSession(models.Model):
    """Manage some security stuffs"""

    _inherit = "pos.session"

    def _loader_params_res_users(self):
        """Insert no_backend_access fields"""
        search_params = super()._loader_params_res_users()
        search_params["search_params"]["fields"].append("no_backend_access")
        return search_params
