# -*- coding utf-8 -*-

from odoo import models, fields ,api
import datetime

class InstanceRequest(models.Model):
    _name = 'instance.request'
    _description = 'demance d_instance'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string='Designation',tracking=True)
    adress_ip = fields.Char(string='Adress Ip')
    _sql_constraints = [
        ("adress_ip_unique", "unique(adress_ip)", "adress ip should be unique choose another one")
    ]
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
    odoo_version_id=fields.Many2one('odoo.version',string='Version odoo')
    odoo_version_ids = fields.Many2many('odoo.version',string='odoo Versions')

    def action_brouillon(self):
        for record in self:
            record.state="brouillon"

    def action_soumise(self):
        for record in self:
            record.state="soumise"

    def action_en_traitement(self):
        for record in self:
            record.state="en_traitement"
            template = self.env.ref("instance_request.instance_request_creation_progress")
            template.send_mail(record.id,
                               email_values={'email_to': record.create_uid.email, 'email_from': self.env.user.email})
            resp_group = self.env.ref('instance_request.group_instance_request_resp')
            users = resp_group.users
            for user in users:
                record.activity_schedule(
                    'instance_request.activity_a_traiter_mail', user_id=user.id, date_deadline=record.limit_date
                )

    def action_traitee(self):
        for record in self:
            record.state="traitee"
            record.treat_date = datetime.date.today()
            template = self.env.ref("instance_request.instance_request_creation")
            template.send_mail(record.id,
                               email_values={'email_to': record.create_uid.email, 'email_from': self.env.user.email})
            record.activity_feedback(['instance_request.activity_a_traiter_mail'])



    @api.model
    def update_sub(self):
        all_records = self.search([])
        for record in all_records:
            jours_restants = (record.limit_date - datetime.date.today()).days
            if jours_restants <= 5 and record.state == "brouillon":
                record.state = "soumise"

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            val['name'] = self.env['ir.sequence'].next_by_code('instance.sequence.code')
            print(val['name'])
        result = super().create(vals_list)

        return result


    @api.model
    def _create_sequence(self):
        sequence = self.env['ir.sequence'].create({
            'name': 'Ma Séquence',
            'code': 'instance.sequence.code',
            'prefix': 'INST',
            'padding': 5
        })
        return sequence

    @api.onchange('limit_date')
    def onchange_limit_date(self):
        if self.limit_date and self.limit_date < fields.Date.today():
            self.limit_date = False
            return {'warning': {'title': _('Error'), 'message': _('You cannot set a deadline in the past.')}}
    def unlink(self):
        if self.state != 'brouillon':
            raise UserWarning('change the state to draft')
        res = super().unlink()
        return res

    def write(self, vals):

        res = super().write(vals)
        for record in self:
            resp_group = self.env.ref('instance_request.group_instance_request_resp')
            users = resp_group.users
            for user in users:
                record.activity_reschedule(['instance_request.activity_a_traiter_mail'],
                date_deadline= record.limit_date,
                                           )
        return res


