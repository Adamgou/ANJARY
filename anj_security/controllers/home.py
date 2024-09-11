from odoo.addons.web.controllers.home import Home as BaseHome
from odoo import http
from odoo.http import request


class Home(BaseHome):
    """Manage access security"""

    @http.route("/web", type="http", auth="none")
    def web_client(self, s_action=None, **kw):
        """Force users with defined pos_config_id to go directly to it's screen."""
        response = super().web_client(s_action, **kw)
        if response.qcontext.get("response_template") == "web.webclient_bootstrap":
            pos_config_id = request.env.user.pos_config_id
            if pos_config_id:
                return request.redirect(pos_config_id.open_ui()["url"])
        return response
