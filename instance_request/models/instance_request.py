# -*- coding utf-8 -*-

from odoo import models, fields ,api
from odoo.exceptions import ValidationError
import datetime

class InstanceRequest(models.Model):
    _name = 'instance.request'
    _description = 'demance d_instance'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string='Designation',tracking=True)
    adress_ip = fields.Char(string='Adress Ip')
    # _sql_constraints = [
    #     ("adress_ip_unique", "unique(adress_ip)", "adress ip should be unique choose another one")
    # ]
    cpu = fields.Integer(string='cpu')
    ram = fields.Integer(string='ram')
    disk = fields.Integer(string='disk')
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
    treat_duration=fields.Integer(string='Treat Duration',compute='_compute_treat_duration', store=1)


    odoo_id=fields.Many2one('odoo.version',string='Version odoo')
    partner_id = fields.Many2one('res.partner', string="Contact")
    tl_id = fields.Many2one('hr.employee', string='Employee')
    tl_user_id =  fields.Many2one(related="tl_id.user_id")
    perimeters_ids = fields.Many2many('instance.perimetre',string='Perimeters')
    nb_perimeters= fields.Integer(string="Nombre Perimeters",compute='_compute_nb_perim')
    devis_ids = fields.One2many('sale.order','insatnce_id', string="Devis")

    @api.depends('treat_date')
    def _compute_treat_duration(self):
        for rec in self:
            if rec.treat_date:
                rec.treat_duration = (rec.treat_date - datetime.date.today()).days
            else:
                rec.treat_duration=0

    @api.depends('perimeters_ids')
    def _compute_nb_perim(self):
        for rec in self:
            rec.nb_perimeters = len(rec.perimeters_ids)


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
            raise ValidationError('You cannot set a deadline in the past.')
    def unlink(self):
        for rec in self :
            if rec.state != 'brouillon':
                raise ValidationError('change the state to draft')
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


    @api.constrains('adress_ip')
    def check_adress(self):
        for record in self :
            adress = self.env['instance.request'].search([('adress_ip','=',record.adress_ip),('id','!=',record.id)])
            if adress :
                raise ValidationError('change the adress_ip')

    def open_insatance_view(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Instance View',
            'res_model': 'instance.request',
            'view_mode': 'list',
        }


