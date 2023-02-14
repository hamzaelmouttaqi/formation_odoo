{
    'name' : 'Instance Request',
    'version' : '16.0',
    'summary': 'Instance Request',
    'sequence': 10,
    'description': """
Instance Request """,
    'website': 'https://www.odoo.com/app/instance_request',
    'depends' : ['base'],
    'data': ['data/data.xml',
             'security/ir.model.access.csv',
             'views/instance_request.xml',
             'views/odoo_version.xml'
    ],
    'application': True,
    'license': 'LGPL-3',
}
