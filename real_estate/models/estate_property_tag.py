from odoo import fields,models

class PropertyTags(models.Model):
    _name = "estate_property_tag"
    _description = "Estate Property Tags"
    _order = "name"

    name = fields.Char(string='Name',required=True)
    color = fields.Integer()
    company_id = fields.Many2one(
        'res.company', string="Company",
        required=True, index=True,
        default=lambda self: self.env.company
    )

    _sql_constraints = [
        ('unique_property_tag_name', 'unique(name)', 'The property tag name must be unique.')
    ]
