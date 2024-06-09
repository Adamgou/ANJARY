/** @odoo-module **/

import { registry } from "@web/core/registry";
import { SaleOrderLineProductField, saleOrderLineProductField } from '@sale/js/sale_product_field';
import { serializeDateTime } from "@web/core/l10n/dates";
import { _t } from "@web/core/l10n/translation";



export class SaleOrderLineProductRentalField extends SaleOrderLineProductField{
    static props = {
        ...SaleOrderLineProductField.props,
        rentField: {type: Boolean, optional: true } 
    };

    async _onProductUpdate() {
        super._onProductUpdate(...arguments);
        if (
            this.props.record.data.is_product_rentable && this.props
        ) {
            // The rental configurator is only expected to open in Rental App
            //      (rent specified true in the xml field options)
            // Allows selling a product in the sale app while also renting it in the Rental app
            this._openRentalConfigurator(false);
        }
    }

    _editLineConfiguration() {
        super._editLineConfiguration(...arguments);
        if (this.props.record.data.is_rental) {
            this._openRentalConfigurator(true);
        }
    }

    get isConfigurableLine() {
        return super.isConfigurableLine || !!this.props.record.data.is_rental;
    }

    configurationButtonFAIcon() {
        if (this.props.record.data.is_rental) {
            return 'fa-calendar';
        }
        return super.configurationButtonFAIcon(...arguments);
    }

    _defaultRentalData(edit) {
        const recordData = this.props.record.data
        let defaultLotIds = recordData.selected_lot_ids.resIds.length > 0 ? [[6, 0, recordData.selected_lot_ids.resIds.map(resId=>resId)]] : false;
        const data = {
            default_quantity: recordData.product_uom_qty,
            default_product_id: recordData.product_id[0],
            default_uom_id: recordData.product_uom[0],
            default_unit_price: recordData.price_unit,
            default_location_price_id: recordData.location_price_id ? recordData.location_price_id[0] : false,
        };
        const saleOrderRecord = this.props.record.model.root;
        if (saleOrderRecord.data.company_id) {
            data.default_company_id = saleOrderRecord.data.company_id[0];
        }
        if (saleOrderRecord.data.pricelist_id) {
            data.default_pricelist_id = saleOrderRecord.data.pricelist_id[0];
        }
        if (saleOrderRecord.data.warehouse_id) { // magical sale_stock_renting default
            data.default_warehouse_id = saleOrderRecord.data.warehouse_id[0];
        }
        if (edit) {
            data.default_pickup_date = serializeDateTime(recordData.start_date);
            data.default_return_date = serializeDateTime(recordData.return_date);

            if (recordData.tax_id) {
                // NOTE: this is not a true default, but a data used by business python code
                data.sale_order_line_tax_ids = recordData.tax_id.records.map(record => record.data.id);
            }

            if (recordData.id) {
                // when editing a rental order line, we need its id for some availability computations.
                data.default_rental_order_line_id = recordData.id;
            }
        } else {
            /** Default pickup/return dates are based on previous lines dates if some exists */
            const saleOrderLines = saleOrderRecord.data.order_line.records.filter(
                line => !line.data.display_type && line.data.is_product_rentable && line.data.is_rental
            );
            let defaultPickupDate, defaultReturnDate;

            if (saleOrderLines.length) {
                saleOrderLines.forEach(function (line) {
                    if (line.data.is_rental) {
                        defaultPickupDate = line.data.start_date;
                        defaultReturnDate = line.data.return_date;
                    }
                });

                if (defaultPickupDate) {
                    data.default_pickup_date = serializeDateTime(defaultPickupDate);
                }
                if (defaultReturnDate) {
                    data.default_return_date = serializeDateTime(defaultReturnDate);
                }
            }
        }
        data.default_lot_ids = defaultLotIds;
        return data;
    }

    async _openRentalConfigurator(edit) {
        this.action.doAction(
            'anj_sale_renting.rental_configurator_action',
            {
                additionalContext: this._defaultRentalData(edit),
                onClose: async (closeInfo) => {
                    if (closeInfo && !closeInfo.special) {
                        this.props.record.update(closeInfo.rentalConfiguration);
                    } else {
                        if (!this.props.record.data.start_date || !this.props.record.data.return_date) {
                            this.props.record.update({
                                product_id: false,
                                name: '',
                            });
                        }
                    }
                }
            }
        );
    }
}

export const saleOrderLineProductRentalField = {
    ...saleOrderLineProductField,
    component: SaleOrderLineProductRentalField,
    supportedOptions: saleOrderLineProductField.supportedOptions.concat([{
        label: _t("Enable product rental configuration"),
        name: "rent",
        type: "boolean",
    }]),
    extractProps(fieldInfo, dynamicInfo) {
        const props = saleOrderLineProductField.extractProps(...arguments);
        props.rentField = fieldInfo.options.rent;
        return props;
    },
};

registry.category("fields").add("sol_product_rental_many2one", saleOrderLineProductRentalField);
