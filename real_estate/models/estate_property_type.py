from odoo import fields,models

class PropertyType(models.Model):
    _name = "estate_property_type"
    _description = "Estate Property Types"
    _order = "sequence,name"

    name = fields.Char(string='Name',default="unknown",required=True)
    sequence = fields.Integer('Sequence')
    property_ids = fields.One2many('real_estate', 'property_type_id')

    _sql_constraints = [
        ('unique_property_type_name', 'unique(name)', 'The property type name must be unique.')
    ]

    

   