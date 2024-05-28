/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";

import { DiscountButton } from "@pos_discount/overrides/components/discount_button/discount_button";

patch(DiscountButton.prototype, {
    async discountPopup(discount_type) {
        var self = this;

        const { confirmed, payload } = await this.showPopup('NumberPopup',{
            title: _t('Discount'),
            startingValue: this.pos.config.discount_pc,
            isInputSelected: true
        });
        if (confirmed) {
            const val = Math.round(Math.max(0,Math.min(100000000,parseFloat(payload))));
            await self.apply_discount(val, discount_type);
        }
    },
    async click() {

        var discount_type = false;

        if (this.pos.config.global_discount_type === 'percentage') {
            discount_type = 'percentage';
        } else if (this.pos.config.global_discount_type === 'amount') {
            discount_type = 'amount';
        } else {
            const { confirmed } = await this.showPopup('ConfirmPopup', {
                title: _t('Select Discount Type'),
                body: _t(
                    'Please select the type of global discount to be applied'
                ),
                confirmText: _t('Percentage'),
                cancelText: _t('Amount'),
            });
            if (confirmed) {
                discount_type = 'percentage';
            }
            else {
                discount_type = 'amount';
            }
        }

        await this.discountPopup(discount_type);
    },
    async apply_discount(pc, discount_type) {
        const order = this.pos.get_order();
        const lines = order.get_orderlines();
        const product = this.pos.db.get_product_by_id(this.pos.config.discount_product_id[0]);
        if (product === undefined) {
            await this.popup.add(ErrorPopup, {
                title: _t("No discount product found"),
                body: _t(
                    "The discount product seems misconfigured. Make sure it is flagged as 'Can be Sold' and 'Available in Point of Sale'."
                ),
            });
            return;
        }

        // Remove existing discounts
        lines
            .filter((line) => line.get_product() === product)
            .forEach((line) => order._unlinkOrderline(line));

        // Add discount
        var discount = 0;
        // Check the type of discount selected
        if (discount_type === 'percentage') {
            // We add the price as manually set to avoid recomputation when changing customer.
            var base_to_discount = order.get_total_without_tax();
            if (product.taxes_id.length){
                var first_tax = this.env.pos.taxes_by_id[product.taxes_id[0]];
                if (first_tax.price_include) {
                    base_to_discount = order.get_total_with_tax();
                }
            }
            discount = - pc / 100.0 * base_to_discount;
        } else {
            discount = - pc;
        }

        if( discount < 0 ){
            order.add_product(product, {
                price: discount,
                lst_price: discount,
                extras: {
                    price_manually_set: true,
                },
            });
        }
    }


})