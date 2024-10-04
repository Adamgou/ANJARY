/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";

patch(PosStore.prototype, {

    getReceiptHeaderData(order) {
        const result = super.getReceiptHeaderData(...arguments);
        result.config = this.config
        return result;
    }
});
