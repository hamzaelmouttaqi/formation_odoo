{
    'name': 'Instance Request',
    'version': '16.0',
    'summary': 'Instance Request',
    'sequence': 10,
    'description': """
Instance Request """,
    'website': 'https://www.odoo.com/app/instance_request',
    'depends': ['base','mail','sale_management','sale','contacts','hr'],
    'data': ['data/data.xml',
             'data/mail_template.xml',
             'data/activity_a_traitee.xml',
             'security/security.xml',
             'security/ir.model.access.csv',
             'views/hr_employee.xml',
             'views/instance_request.xml',
             'views/odoo_version.xml',
             'views/perimetres.xml',
             'views/devis.xml',
             'wizards/instance_wizard.xml',
             'reports/insatance_request_report.xml'

             ],
    'application': True,
    'license': 'LGPL-3',
}
