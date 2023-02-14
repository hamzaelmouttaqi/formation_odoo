from odoo import models, fields

class InstanceRequest(models.Model):
    _name = 'odoo.version'
    _description = 'odoo version'

    version = fields.Char(string='Version')