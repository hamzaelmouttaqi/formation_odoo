from odoo import models, fields,api

class HrEmployee(models.Model):
    _inherit ='hr.employee'

    instance_ids =fields.One2many('instance.request','tl_id' ,string='Instance Request',tracking=True)
    nb_instance = fields.Integer(string="Nombre Instance", compute='_compute_nb_instance')

    @api.depends('instance_ids')
    def _compute_nb_instance(self):
        for rec in self:
            rec.nb_instance = len(rec.instance_ids)

    def action_related_insatnce(self):
        self.ensure_one()
        return {
            'name': "Related Instance",
            'type': 'ir.actions.act_window',
            'view_mode': 'kanban,tree,form',
            'res_model': 'instance.request',
            'domain': [('id', 'in', self.instance_ids.ids)]
        }