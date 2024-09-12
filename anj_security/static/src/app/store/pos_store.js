/* @odoo-module */

import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";

patch(PosStore.prototype, {
    redirectToBackend() {
        if (!this.user.no_backend_access) {
            return super.redirectToBackend()
        }
        window.location = "/web/session/logout";
    }
})
