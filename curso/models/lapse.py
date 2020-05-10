# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution.
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>...
#
##############################################################################
from openerp import models, fields, api


class curso_lapse(models.Model):
    """ Define un lapso de tiempo se usa como clase abstracta """
    _name = 'curso.lapse'

    start_time = fields.Float(
        string='Desde',
        required=True
    )

    formatted_start_time = fields.Char(
        compute='_compute_start_time'
    )

    end_time = fields.Float(
        string='Hasta',
        required=True
    )

    elapsed_time = fields.Float(
        compute='_compute_elapsed_time',
        string='Duración'
    )

    def _compute_elapsed_time(self):
        for rec in self:
            rec.elapsed_time = rec.end_time - rec.start_time

    @api.depends('start_time')
    def _compute_start_time(self):
        for rec in self:
            t = rec.start_time
            mm = t - int(t)
            hh = t - mm
            rec.formatted_start_time = "{:0>2d}:{:0>2d}".format(int(hh),
                                                                int(mm * 60))
