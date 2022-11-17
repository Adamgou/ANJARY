odoo.define('anj_sale_renting.RentalConfiguratorFormController', function(require){
    "use strict";

    var RentalConfiguratorFormController = require('sale_renting.RentalConfiguratorFormController');


    RentalConfiguratorFormController.include({
        _getRentalInfo: function (state) {
            return {
                pickup_date: state.pickup_date,
                return_date: state.return_date,
                price_unit: state.unit_price,
                product_uom_qty: state.quantity,
                discount: 0.0,
                is_rental: true,
                selected_lot_ids: this._anjConvertFromMany2Many(state.lot_ids),
            };
        },
        _anjConvertFromMany2Many: function (recordData) {
            if (recordData) {
                var convertedValues = [];
                _.each(recordData.res_ids, function (resId) {
                    convertedValues.push([4, parseInt(resId)]);
                });
    
                return convertedValues;
            }
    
            return null;
        },
    });

    return RentalConfiguratorFormController;
})