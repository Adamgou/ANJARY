# -*- coding: utf-8 -*-

from odoo import models


class PosSession(models.Model):
    _inherit = "pos.session"

    def _loader_params_res_company(self):
        params = super()._loader_params_res_company()
        params["search_params"]["fields"].append("is_biskot")
        return params
