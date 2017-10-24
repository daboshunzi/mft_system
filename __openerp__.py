# -*- coding: utf-8 -*-

{
    # The human-readable name of your module, displayed in the interface
    'name': "Manufacture System",
    # A more extensive description
    'description': """
    """,
    # Which modules must be installed for this one to work
    #'depends': ['base'],
    'depends': ['base'],
    'data': [
        #'templates.xml',
        'mft_security.xml',
        'ir.model.access.csv',
        'views.xml',
        'mft_sequence.xml'
    ],
    'demo':[
    ],
}