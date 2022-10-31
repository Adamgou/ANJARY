odoo.define('anj_sale_renting.rental_configurator', function (require) {
    const ProductConfiguratorWidget = require('sale_renting.rental_configurator');
    ProductConfiguratorWidget.include({
        _defaultRentalData: function (data) {
            data = this._super.apply(this, data)
            data.default_sale_order_id = this.record.evalContext.parent.id;
            return data;
        }
    });

    return ProductConfiguratorWidget;

}); 