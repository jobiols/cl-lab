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
from datetime import datetime, timedelta

from openerp import models, fields, api


class curso_schedule(models.Model):
    """ horarios que puede tener un curso """
    _name = 'curso.schedule'
    _inherit = 'curso.lapse'
    _sql_constraints = [
        ('default_code_unique', 'unique (name)', 'Este horario ya existe.')]

    name = fields.Char(
        compute="_get_name",
        store=True
    )

    @staticmethod
    def _calc_datetime(_date, _time):
        mm = _time - int(_time)
        hh = int(_time - mm)
        mm = int(mm * 60)

        tt = datetime(_date.year, _date.month,
                      _date.day, hh, mm, tzinfo=None)

        # aca sumamos tres horas porque es UTC
        # el campo le resta tres horas.
        tt = tt + timedelta(hours=3)
        return tt.strftime("%Y-%m-%d %H:%M:%S")

    def start_datetime(self, date):
        return self._calc_datetime(date, self.start_time)

    def stop_datetime(self, date):
        return self._calc_datetime(date, self.end_time)

    @staticmethod
    def _f2h(t):
        mm = t - int(t)
        hh = t - mm
        return "{:0>2d}:{:0>2d}".format(int(hh), int(mm * 60))

    @staticmethod
    def _f2hh_mm(t):
        mm = t - int(t)
        hh = t - mm
        mm *= 60
        if int(mm) == 0:
            res = "{}hs".format(int(hh))
        else:
            res = "{}hs {}min".format(int(hh), int(mm))
        return res

    @api.depends('start_time', 'end_time')
    def _get_name(self):
        for rec in self:
            aa = self._f2h(rec.start_time)
            bb = self._f2h(rec.end_time)
            cc = self._f2hh_mm(rec.end_time - rec.start_time)
            rec.name = "{} - {} ({})".format(aa, bb, cc)
