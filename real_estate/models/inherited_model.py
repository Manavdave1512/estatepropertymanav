from odoo import fields, models

class InheritedModel(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("real_estate","sales_man") 
    
