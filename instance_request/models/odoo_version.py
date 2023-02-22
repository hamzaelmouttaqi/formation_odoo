from odoo import models, fields,api

class OdooVersion(models.Model):
    _name = 'odoo.version'
    _description = 'odoo version'

    name = fields.Char(string='Version')
    instance_odoo_ids = fields.One2many('instance.request', 'odoo_id', string='Instance Request',
                                   )
    nb_instance_odoovers = fields.Integer(string="Nombre Instance", compute='_compute_nb_instance')

    @api.depends('instance_odoo_ids')
    def _compute_nb_instance(self):
        for rec in self:
            rec.nb_instance_odoovers = len(rec.instance_odoo_ids)
