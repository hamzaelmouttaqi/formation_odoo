# -*- coding utf-8 -*-
from odoo import models, fields ,api
import datetime

class InstanceRequest(models.Model):
    _name = 'instance.request'
    _description = 'demance d_instance'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string='Designation',tracking=True)
    adress_ip = fields.Char(string='Adress Ip')
    cpu = fields.Char(string='cpu')
    ram = fields.Char(string='ram')
    disk = fields.Char(string='disk')
    url = fields.Char(string='url')
    active = fields.Boolean(string='Is_Active',default='True')
    state = fields.Selection(
        [
            ("brouillon", "Draft"),
            ("soumise", "Submitted"),
            ("en_traitement", "In Process"),
            ("traitee", "Done")
        ],
        default='brouillon',tracking=True)
    limit_date = fields.Date(string='Limit Date',tracking=True)
    treat_date=fields.Date(string='Treat Date')
    treat_duration=fields.Float(string='Treat Duration')

    def action_brouillon(self):
        for record in self:
            record.state="brouillon"

    def action_soumise(self):
        for record in self:
            record.state="soumise"

    def action_en_traitement(self):
        for record in self:
            record.state="en_traitement"

    def action_traitee(self):
        for record in self:
            record.state="traitee"

    @api.model
    def update_sub(self):
        all_records = self.search([])
        for record in all_records:
            jours_restants = (record.limit_date - datetime.date.today()).days
            if jours_restants <= 5 and record.state == "brouillon":
                record.state = "soumise"
