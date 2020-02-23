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
import locale
from datetime import datetime, timedelta

#from openerp import SUPERUSER_ID
#from openerp import api
#from openerp.osv import osv
from odoo import models

try:
    locale.setlocale(locale.LC_ALL, 'es_AR.utf8')
except:
    pass


class CursoInformation(models.Model):
    """ Wizard para generar documentacion de los cursos
    """
    _name = 'curso.information'
    _description = __doc__

    def button_information(self):
        curso_obj = self.env['curso.curso']
        for curso in curso_obj.browse(self._context.get('active_ids',[])):
            curso.button_generate_doc_curso()
        return True


class CursoCurso(models.Model):
    """ Representa una instancia de un curso
    """
    _name = 'curso.curso'
    _description = __doc__
    _order = 'date_begin'
    _inherit = ['mail.thread'] #documents.mixin

    class weekdays():
        _weekload = []
        _ix = 0

        def __init__(self, wl, date):
            # ordering the weekload by weekday
            wl.sort(key=lambda b: b['weekday'])

            self._weekload = wl
            self._start_date = self._current_date = date

            # adjust ix to point the right weekday
            start_weekday = int(self._start_date.strftime('%w'))
            for ix in range(len(wl)):
                if start_weekday == wl[ix]['weekday']:
                    self._ix = ix

        def get_date(self):
            return self._current_date

        def get_schedule(self):
            return self._weekload[self._ix]['schedule']

        def get_room(self):
            return 'A'

        def _gwd(self, ix):
            return self._weekload[ix]['weekday']

        def next_class(self):

            # move ix one ahead
            ix_1 = self._ix
            self._ix += 1
            if self._ix >= len(self._weekload):
                self._ix = 0
            ix = self._ix

            # calculate current date
            if self._gwd(ix) > self._gwd(ix_1):
                self._current_date += timedelta(days=self._gwd(ix) - self._gwd(ix_1))
            else:
                self._current_date += timedelta(
                        days=7 - (self._gwd(ix_1) - self._gwd(ix)))

    def generate_doc_curso_html(self, dict):
        ret = ""
        ret += "  	<style type=\"text/css\">th"
        ret += "{"
        ret += "                background-color: white;"
        ret += "                color: black;"
        ret += "                text-align: center;"
        ret += "                vertical-align: bottom;"
        ret += "                height: 100px;"
        ret += "                padding-bottom: 3px;"
        ret += "                padding-left: 2px;"
        ret += "                padding-right: 2px;"
        ret += "            }"

        ret += "            .verticalText"
        ret += "            {"
        ret += "                text-align: center;"
        ret += "                vertical-align: middle;"
        ret += "                width: 18px;"
        ret += "                margin: 0px;"
        ret += "                padding: 0px;"
        ret += "                padding-left: 1px;"
        ret += "                padding-right: 1px;"
        ret += "                padding-top: 5px;"
        ret += "                white-space: nowrap;"
        ret += "                -webkit-transform: rotate(-90deg);"
        ret += "                -moz-transform: rotate(-90deg);"
        ret += "            };"
        ret += "</style>"

        ret += "<table border=\"1\">"
        ret += "	<tbody>"
        ret += "		<tr>"
        ret += "			<th width=\"200px;\">"
        ret += "			<div>" + dict['titulo'] + "</div>"
        ret += "			</th>"
        for clase in dict['clases']:
            ret += "			<th>"
            ret += "			<div class=\"verticalText\">" + clase['fecha'] + "</div>"
            ret += "			</th>"

        ret += "		</tr>"
        for alumna in dict['alumnas']:
            ret += "		<tr>"
            state = '(Sin Confirmar)' if alumna.get('state') != 'confirm' else ''
            ret += "			<td>{} {}</td>".format(alumna.get('name'), state)
            for fecha in dict['clases']:
                ret += "			<td>&nbsp;</td>"

            ret += "		</tr>"

        ret += "	</tbody>"
        ret += "</table>"
        ret += "<h2><br/><br/>Temario</h2>"
        ret += "<table border=\"0\" cellpadding=\"1\" cellspacing=\"1\" style=\"width: 100%;\">"
        ret += "	<tbody>"
        for clase in dict['clases']:
            ret += "		<tr>"
            ret += "			<td>" + clase['fecha'] + "&nbsp;</td>"
            if clase['name']:
                dd = clase['name']
            else:
                dd = "no hay tema"
            ret += "			<td>" + dd + "</td>"
            ret += "		</tr>"
        ret += "</tbody>"
        ret += "</table>"

        return ret

    def button_generate_doc_curso(self):
        """ Genera planilla de asistencia para el curso
        """
        for curso in self:
            alumnas = []
            reg_pool = self.env['curso.registration']

            # mostrar las alumnas confirmada y señadas
            records = reg_pool.search([('curso_id', '=', curso.id), '|',
                                       ('state', '=', 'confirm'),
                                       ('state', '=', 'signed')])
            for reg in records:
                alumnas.append({
                    'name': reg.partner_id.name,
                    'credit': reg.partner_id.credit,
                    'state': reg.state})

            clases = []
            lect_pool = self.env['curso.lecture']
            records = lect_pool.search([('curso_id', '=', curso.id)],
                                       order="date")
            for lect in records:
                d = {'fecha': datetime.strptime(
                            lect.date, "%Y-%m-%d").strftime("%d/%m/%y"),
                     'name': lect.name}
                clases.append(d)

            data = {
                'titulo': curso.curso_instance,
                'alumnas': alumnas,
                'clases': clases,
            }

            new_page = {
                'name': curso.name,
                'content': self.generate_doc_curso_html(data),
            }

            # Borrar el documento si es que existe
            doc_pool = self.env['document.page']
            records = doc_pool.search([('name', '=', curso.name)])
            records.unlink(records)

            # Generar el documento
            self.env['document.page'].create(new_page)

        return True

    def copy(self, default=None):
        """ Reset the state and the registrations while copying an curso
        """
        if not default:
            default = {}

        default.update({
            'state': 'draft',
            'registration_ids': False,
        })
        return super().copy(default=default)

    def get_weekload(self):
        ret = []
        for curso in self:
            diary_obj = self.env['curso.diary']
            for day in diary_obj.search([('curso_id', '=', curso.id)]):
                ret.append({
                    'weekday': int(day.weekday),
                    'schedule': day.schedule
                })
        return ret

    # Estados de los cursos
    ###############################################################################

    def button_curso_done(self):
        """
        Terminar el curso
        """
        # si existe al menos una en estado signed no se puede terminar el curso
        # si existe al menos una en estado confirm no se puede terminar el curso
#        reg_obj = self.pool.get('curso.registration')
#        reg_ids = reg_obj.search(cr, uid,
#                                 [('curso_id', 'in', ids),
#                                  '|',
#                                  ('state', '=', 'signed'),
#                                  ('state', '=', 'confirm')
#                                  ], context=context)
#        if reg_ids:
#            raise osv.except_osv(
#                    'Error!',
#                    u"Para terminar el curso las alumnas deben estar en estado \
#                    cumplido, o cancelado.")

        # si existe al menos una en estado signed o confirm no se puede
        # terminar el curso
        chk = self.registration_ids.search([('state','in',['signed','confirm'])])
        if chk:
            raise UserWarning("Para terminar el curso las alumnas deben estar "
                              "en estado cumplido, o cancelado.")

        # si existen interesadas hay que proponer moverlas a otro curso
        chk = self.registration_ids.search([('state','not in',['done','cancel','draft'])])
        if chk:
            raise UserWarning(u"Para terminar el curso las alumnas deben "
                              u"estar en estado cumplido, cancelado o "
                              u"interesada. Usá el menú Mover / Copiar para "
                              u"pasarlas a otro curso")

        return self.write({'state': 'done'})

    def button_curso_cancel(self):
        """ Cancelar el curso.
        """
        # si existe al menos una en estado signed no se puede cancelar el curso
        # si existe al menos una en estado confirm no se puede cancelar el curso
        # si existe al menos una en estado cumplido no se puede cancelar el curso

        # chequear que todas las alumnas estan canceladas
        chk = self.registration_ids.search([('state', 'not in', 'cancel')])
        if chk:
            raise UserWarning('No se puede cancelar el curso si hay alumnas '
                              'en estado Señado, cumplido o cursando')

        # borrar todas las clases
        self.lecture_ids.unlink()

        return self.write({'state': 'cancel'})

    def get_holiday_dates(self):
        hd = []
        for holiday in self.env['curso.holiday'].search([]):
            hd.append(datetime.strptime(holiday.date, '%Y-%m-%d'))
        return hd

    def lectures_list(self, weekdays, no_lectures):
        ret = []
        for ix in range(no_lectures):
            ret.append((
                weekdays.get_date(),
                weekdays.get_schedule(),
                weekdays.get_room()))
            weekdays.next_class()
        return ret

    def lecture_overlaps(self, date, schedule, room):
        return False

    def get_lecture_templates(self, product_id):
        template_obj = self.env['curso.lecture_template']

        ret = []
        for rec in template_obj.search([('product_id', '=', product_id)]):
            ret.append({'name': rec.text})

        return ret

    def onchange_curso_product(self, product):
        values = {}
        if product:
            records = self.env['curso.curso'].search(
                [('default_code', '=', product.default_code)])

            instance = 0
            for item in records:
                if item:
                    if (instance < item.instance):
                        instance = item.instance
            instance += 1
            values.update({
                'instance': instance,
            })
        return {'value': values}

    def clone_diary(self, curso_from, curso_to):
        diary_obj = self.env['curso.diary']
        diarys = diary_obj.search([('curso_id', '=', curso_from)])
        for diary in diarys:
            diary_obj.create({
                'curso_id': curso_to,
                'weekday': diary.weekday,
                'schedule': diary.schedule.id,
                'seq': diary.seq
            })

    def button_update_child_from_parent(self, parent_id, class_id):
        """ Update child with parent information
            date_begin: the date of the lecture the child is inserted on
            diary_id: create the same diary as parent
            child: True
        """
        res = {}
        for curso in self:
            self.clone_diary(parent_id, curso.id)
            lecture_obj = self.env['curso.lecture']
            for lecture in lecture_obj.search([('id', '=', class_id)]):
                res['date_begin'] = lecture.date

#    def subscribe_to_curso(self, cr, uid, ids, context=None):
#        register_pool = self.pool.get('curso.registration')
#        user_pool = self.pool.get('res.users')
#        num_of_seats = int(context.get('ticket', 1))
#        user = user_pool.browse(cr, uid, uid, context=context)
#        curr_reg_ids = register_pool.search(cr, uid, [('user_id', '=', user.id),
#                                                      ('curso_id', '=', ids[0])])
        # the subscription is done with SUPERUSER_ID because in case we share the
        # kanban view, we want anyone to be able to subscribe
#        if not curr_reg_ids:
#            curr_reg_ids = [register_pool.create(cr, SUPERUSER_ID,
#                                                 {'curso_id': ids[0], 'email': user.email,
#                                                  'name': user.name,
#                                                  'user_id': user.id,
#                                                  'nb_register': num_of_seats})]
#        else:
#            register_pool.write(cr, uid, curr_reg_ids, {'nb_register': num_of_seats},
#                                context=context)
#        return register_pool.confirm_registration(cr, SUPERUSER_ID, curr_reg_ids,
#                                                  context=context)

#    def unsubscribe_to_curso(self, cr, uid, ids, context=None):
#        register_pool = self.pool.get('curso.registration')
#        # the unsubscription is done with SUPERUSER_ID because in case we share the
#        # kanban view, we want anyone to be able to unsubscribe
#        curr_reg_ids = register_pool.search(cr, SUPERUSER_ID, [('user_id', '=', uid),
#                                                               ('curso_id', '=', ids[0])])
#        return register_pool.button_reg_cancel(cr, SUPERUSER_ID, curr_reg_ids,
#                                               context=context)
