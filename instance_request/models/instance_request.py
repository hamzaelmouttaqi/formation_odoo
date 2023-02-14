from odoo import models, fields

class InstanceRequest(models.Model):
    _name = 'instance.request'
    _description = 'demance d_instance'

    name = fields.Char(string='Designation')
    adress_ip = fields.Char(string='Adress Ip')
    cpu = fields.Char(string='cpu')
    ram = fields.Char(string='ram')
    disk = fields.Char(string='risk')
    url = fields.Char(string='url')
    active = fields.Boolean(string='Is_Active',default='True')
    state = fields.Selection([('Brouillon','Brouillon'),('Soumise','Soumise'), ('En traitement','En traitement'),
                              ('Traitée','Traitée')],string='State',default='Brouillon')
    limit_date = fields.Date(string='Limit Date')
    treat_date=fields.Date(string='Treat Date')
    treat_duration=fields.Float(string='Treat Duration')