{
    'name': 'Real Estate Management',
    'version': '1.0',
    'summary': 'Manage properties, buyers, and sales in real estate',
    'author': 'Manav Dave',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        
        'views/estate_property_views.xml',
        'views/estate_property_tag_views.xml',
         'views/inherited_res_user_model_views.xml',
         'views/estate_property_kanban.xml',
         'reports/estate_property_report_action.xml',
         'reports/estate_property_report_template.xml',
         'views/estate_menus.xml',
        ],
    # "demo": [
    #     "data/estate_demo.xml"
    # ],    
    'installable': True,
    'application': True,
}
