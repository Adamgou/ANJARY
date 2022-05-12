from odoo import models, fields, api,_
class Sale_order_line(models.Model):
    _inherit="sale.order.line"
    location_price_id = fields.Many2one(
        comodel_name='location.price',
        string='Prix de location',
        required=False)

    

    @api.onchange('location_price_id')
    def onchange_location_price(self):
        self.price_unit=self.location_price_id.location_price

    

class Sale(models.Model):
    _inherit='sale.order'

    is_transfert = fields.Boolean('Transfert')

    hotel_partner = fields.Char(
        string='Hotel partenaire', default="Anjary Hotel",
        required=False)

    transfert_date = fields.Date(
        string='Date de transfert',
        required=False)

    fligth_company = fields.Char(
        string='Companie aériène',
        required=False)

    # immatriculation
    car_registration = fields.Char('Plaque véhicule')

    # nom complet du chauffeur
    # driver_name = fields.Char('Driver Name')
    employee_id = fields.Many2one('hr.employee', string='Conducteur')

    # liste initial de passager
    passenger_list_ids = fields.One2many('passenger.list.praxi', 'passenger_sale_order_id', string='Liste de passager')
    passenger_additive_list_ids = fields.One2many('passenger.list.additive', 'passenger_additive_sale_order_id', string='Liste additive des passagers')
    is_additive_passenger = fields.Boolean('Liste additive')
    # liaison sale order
    sale_order_id = fields.Many2one('sale.order', string='Sale Order')

    def action_sms(self):
        date= self.date_order.strftime("%d/%m/%Y")
        driver=self.employee_id.name or ''
        registration_car=self.car_registration or ''

        template_sms=f"""Bonjour {self.partner_id.name}. Votre commande a été confirmée pour le {date}. Véhicule {registration_car}. Chauffeur : {driver}. Praxi vous remercie pour votre confiance."""

        ctx = self._context.copy()
        
        print(ctx)
        if self.partner_id.mobile:
            tel_phone=self.partner_id.mobile
        elif self.partner_id.phone:
            tel_phone=self.partner_id.phone


        ctx.update({'default_recipient_single_number_itf': tel_phone, 'default_body': template_sms})

        return {

            'type': 'ir.actions.act_window', 

            'view_type': 'form', 

            'view_mode': 'form',

            'res_model': 'sms.composer', 

            'target': 'new', 

            'context':ctx,

        }
    # @api.onchange('partner_id')
    # def _onchange_partner_id(self):
    #     if self.partner_id.employee_id and self.company_id.id == 1:
    
    #         self.employee_id=self.partner_id.employee_id
    #     else:
    #         pass


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

