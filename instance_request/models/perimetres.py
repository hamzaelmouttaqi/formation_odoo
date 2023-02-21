# -*- coding utf-8 -*-
from odoo import models, fields

class Perimetres(models.Model):
    _name = 'instance.perimetre'
    _description = 'perimetre'

    name = fields.Char(string='Nom Périmètres')