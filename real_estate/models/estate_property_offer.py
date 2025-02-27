from odoo import fields,models,api
from datetime import datetime
from datetime import timedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class PropertyOffer(models.Model):
    _name = "estate_property_offer"
    _description = "Estate Property Offers"
    _order = "price desc"
    
    price = fields.Float(string='Price')
    validity = fields.Integer(string="Validity",default=7)
    date_deadline = fields.Date(string="Date Deadline",compute="_compute_date_deadline",inverse="_inverse_date_deadline",store=True)
    statuss = fields.Selection(
    string="Status",
    selection=[
        
        ('acc', 'Accepted'),
        ('ref', 'Refused')
    ],
    copy=False
)  
    company_id = fields.Many2one(
        'res.company', string="Company",
        required=True, index=True,
        default=lambda self: self.env.company
    )
    

    partner_id = fields.Many2one("res.partner",string="Partner",required=True)
    property_id = fields.Many2one("real_estate",string="Property",required=True)
    
    @api.depends('create_date','validity')
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)
    
    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                create_date = record.create_date.date() if record.create_date else fields.Date.today()
            
                record.validity = (record.date_deadline-create_date).days    
    

    def ref(self):
       for offer in self: 
        if offer.statuss != 'acc':
            offer.statuss = 'ref'
        else:
            raise UserError("Accepted property cannot be refused")    

    
    def acc(self):
       for offer in self: 
          for record in self:
            if record.statuss != 'ref':                    
                record.statuss = 'acc'
                record.property_id.selling_price = record.price
                record.property_id.buyer = record.partner_id
            else:
                raise exceptions.UserError('Refused property cannot be accept!')
        

    @api.constrains('price')
    def _check_offer_price(self):
        for record in self:
            if record.price <= 0:
                raise ValidationError("The offer price must be strictly positive.")

    def create(self, vals):
        print(vals)
        for record in vals:

            if (self.env['real_estate'].browse((record['property_id'])).state == 'new'):
                self.env['real_estate'].browse((record['property_id'])).state = 'offerrecieved'

            if (self.env['real_estate'].browse((record['property_id'])).best_price>record['price']):
                raise UserError("The price shold be higher than " + str(self.env['real_estate'].browse((record['property_id'])).best_price))    
            return super().create(vals)  
    
    