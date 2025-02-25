from odoo import models,fields,Command

class InheritedModel(models.Model):
    _inherit = "real_estate"
    
    move_type = fields.Selection(selection=[
            
            ('out_invoice', 'Customer Invoice'),
            
        ], string='Type', required=True)

    def soldb(self):
        print("hello")
        
        property_invoice = {
            'move_type':'out_invoice',
            "name": super().name,
            'invoice_line_ids':[
                Command.create({
                    "name": super().name,
                    'price_unit':super().selling_price,
                    'quantity':1
                }),
                Command.create({
                    "name": "6 %",
                    'price_unit':super().selling_price*0.06,
                    'quantity':1
                }),
                Command.create({
                    'name':"Additonal Charges",
                    'price_unit':100,
                    'quantity':1
                })
            ]
        }
        print(super().name)
        self.env["account.move"].create(property_invoice)
        return super().soldb()
