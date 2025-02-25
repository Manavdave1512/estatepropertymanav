from odoo import fields,models,api
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class Real(models.Model):
    _name = "real_estate"
    _description = "estate model"
    _order = "id desc"

    name = fields.Char(string='Title',default="unknown",required=True)
    
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    
    date_availability = fields.Date(string='Available Dates',default=lambda self: fields.Date.to_string(datetime.today() + relativedelta(months=3)),readonly=True,copy=False)
    expected_price = fields.Float(string ='Expected Price',required=True)
    last_seen = fields.Date(string="Last Seen",default=fields.Datetime.now)
    selling_price = fields.Float(string='Selling Price', copy=False,readonly=True)
    bedrooms = fields.Integer(string='Bedrooms',default=2)
    living_area = fields.Integer(string='Living Area')
    facades = fields.Char(string="Facades",default=0)
    
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string="Garden Area")
    active = fields.Boolean(string="Active",default=False)
    garden_orientation= fields.Selection(
    string="Direction",
    selection=[
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ],
    default = False,
    help="Select the direction"
)


    total_area = fields.Integer(string = "Total Area",compute="_total")
    
    

    state = fields.Selection(
        string = "State",
        selection = [
            ('new','New'),
            ('offerrecieved','Offer Received'),
            ('offerAccepted','Offer Accepted'),
            ('sold','Sold'),
            ('cancelled','Cancelled'),
        ],
        default = "new"
    )
    
    
    buyer = fields.Many2one("res.partner",string="Buyer", copy=False)
    sales_man = fields.Many2one("res.users",string="Sales Man",default=lambda self: self.env.user)
    property_type_id = fields.Many2one("estate_property_type",string="Property Type")
    tag_ids = fields.Many2many("estate_property_tag")
    test_ids = fields.One2many("estate_property_offer", "property_id", string="Tests")
        
    best_price = fields.Integer(string ="Best Offer",compute="_highest",store=True)

    @api.depends('living_area','garden_area')
    def _total(self):
      for record in self:
          record.total_area = record.living_area + record.garden_area

    @api.depends('test_ids.price')
    def _highest(self):
        for record in self:
            record.best_price = max(record.test_ids.mapped('price'),default=0)      

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'

        else:
            self.garden_area = 0
            self.garden_orientation = False    
    
    def soldb(self):
        if self.state == 'cancelled':
            raise UserError("A Cancelled Property Cannot Be Sold")
        self.state = 'sold'    


    def cancelledb(self):
        if self.state == 'sold':
            raise UserError("A sold Property Cannot Be Cancelled")
        self.state = 'cancelled'    



    @api.constrains('expected_price')
    def _check_offer_price(self):
        for record in self:
            if record.expected_price<= 0:
                raise ValidationError("The offer price must be strictly positive.")


    @api.constrains('selling_price')
    def _check_diff(self):
        for record in self:
            if record.selling_price>0 and record.selling_price < (0.9 * record.expected_price):
                raise ValidationError("Selling Price cannot be lower than 90 percent of the expected price")            


    @api.ondelete(at_uninstall=False)
    def _preventdelete(self):
        for record in self:
            if record.state not in ['new','cancelled']:
                raise UserError("Only new and cancelled property can be deleted")

        # return super().unlink()        

    
    


    
               
              