from odoo import models, fields

class OdooVersion(models.Model):
    _name = 'odoo.version'
    _description = 'odoo version'

    name = fields.Char(string='Version')