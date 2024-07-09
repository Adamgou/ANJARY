/* @odoo-module */

import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { threadActionsRegistry } from "@mail/core/common/thread_actions";
import "@mail/discuss/call/common/thread_actions";

const callButton = threadActionsRegistry.get("call");
patch(callButton, {
    condition(component) {
        return false;
    },
});