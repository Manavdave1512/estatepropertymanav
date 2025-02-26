from odoo import fields,models,api

class PropertyType(models.Model):
    _name = "estate_property_type"
    _description = "Estate Property Types"
    _order = "sequence,name"

    name = fields.Char(string='Name',default="unknown",required=True)
    sequence = fields.Integer('Sequence')
    property_ids = fields.One2many('real_estate', 'property_type_id')
    test_ids = fields.One2many("estate_property_offer", "property_id", string="Tests")
    offer_count = fields.Integer('Offers' ,compute="_compute_countoffer")
      
    _sql_constraints = [
        ('unique_property_type_name', 'unique(name)', 'The property type name must be unique.')
    ]

    @api.depends('test_ids')
    def _compute_countoffer(self):
        for record in self:
            record.offer_count = len(record.test_ids)
    
    

   