from odoo import models, fields, api,_
class Sale_order_line(models.Model):
    _inherit="sale.order.line"
    location_price_id = fields.Many2one(
        comodel_name='location.price',
        string='Location price',
        required=False)

    

    @api.onchange('location_price_id')
    def onchange_location_price(self):
        self.price_unit=self.location_price_id.location_price

    

class Sale(models.Model):
    _inherit='sale.order'

    is_transfert = fields.Boolean('Transfert')

    hotel_partner = fields.Char(
        string='Partner hotel',
        required=False)

    transfert_date = fields.Date(
        string='Transfert date',
        required=False)

    fligth_company = fields.Char(
        string='Company operating the flight',
        required=False)

    # immatriculation
    car_registration = fields.Char('Car registration')

    # nom complet du chauffeur
    # driver_name = fields.Char('Driver Name')
    employee_id = fields.Many2one('hr.employee', string='Driver')

    # liste initial de passager
    passenger_list_ids = fields.One2many('passenger.list.praxi', 'passenger_sale_order_id', string='Passenger List')
    passenger_additive_list_ids = fields.One2many('passenger.list.additive', 'passenger_additive_sale_order_id', string='Passenger List')
    is_additive_passenger = fields.Boolean('Liste additive')
    # liaison sale order
    sale_order_id = fields.Many2one('sale.order', string='Sale Order')


    # origin = fields.Char('Origin')
    # def redirect_order_transfert(self):
    #     # import pudb; pudb.set_trace()
    #     ctx = self._context.copy()
    #     ctx['origin'] = self.name
        
    #     return {
    #         'name': _('Transfert order'),
    #         'type': 'ir.actions.act_window',
    #         'view_mode': 'form',
    #         'res_model': 'order.transfert',
    #         'view_id': self.env.ref('anj_location.view_order_transfert_view').id,
    #         'context': ctx,
    #     }

