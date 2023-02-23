# -*- coding utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class InstanceWizard(models.TransientModel):
    _name = 'instance.wizard'
    _description = 'Instance Wizard'

    devis_ids = fields.Many2many('sale.order', string="Devis")
    cpu = fields.Char(string='cpu')
    ram = fields.Char(string='ram')
    disk = fields.Char(string='disk')
    tl_id = fields.Many2one('hr.employee', string='Employee')

    # def apply_odoo_version(self):
    #     for partner in self.partner_ids:
    #         partner.odoo_version_id = self.odoo_version_id.id
    def apply_instance(self):
        if self.cpu <= 0 or self.ram <= 0 or self.disk <= 0:
            raise ValidationError("you can't create an instance with a null performance")
        vals={
            # 'name': 'lk',
            # 'limit_date':'2023-02-28',
            'cpu' :self.cpu,
            'disk' :self.disk,
            'ram': self.ram,
            'tl_id' :self.tl_id.id
            # 'devis_ids' : self.devis_ids
        }
        model1 =   self.env['instance.request'].create(vals)
        return  model1.open_insatance_view()


