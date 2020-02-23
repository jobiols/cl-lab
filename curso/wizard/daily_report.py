# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from datetime import datetime

#from openerp.osv import osv, fields
from odoo import models, fields


class curso_daily_report(models.Model):
    _name = "curso.daily.report"
    _description = "Reporte diario de alumnas"

    date = fields.Date(
        string='Fecha',
        required=True,
        help=u"La fecha para la que se va a generar el reporte"
    )

    def missing_data(self, alumna):
        ret = u''
        if alumna.partner_id.document_number == False:
            ret += u' Documento'
        if alumna.partner_id.street == False:
            ret += u' Dirección'
        if alumna.partner_id.date == False:
            ret += u' Fecha de nacimiento'
        if alumna.partner_id.email == False:
            ret += u' Mail'
        if alumna.partner_id.mobile == False:
            ret += u' Celular'
        if ret != '':
            ret = 'Falta ' + ret

        return ret

    # TODO Refactorizar esto
    def generate_local_html(self, data):

        ret = ""
        for dict in data:
            ret += "<hr/>"
            ret += "<p3><strong>" + dict['curso'] + "</strong><br>"
            ret += dict['tema'] + "</p>"
            ret += "<table border=\"0\" cellpadding=\"1\" cellspacing=\"1\" style=\"width:100%;\">"
            ret += "	<tbody>"
            for alumna in dict['alumnas']:
                ret += "		<tr>"
                ret += "			<td>" + alumna.partner_id.name + "</td>"
                ret += "			<td>" + str(alumna.partner_id.email) + "</td>"
                ret += "			<td>" + str(alumna.partner_id.mobile) + "</td>"
                ret += "		</tr>"
            ret += "	</tbody>"
            ret += "</table>"
            ret += "<br>"

        ret += "<hr/>"
        ret += '<table border="0" cellpadding="0" cellspacing="0" style="width:100%;">'
        ret += '    <tbody>'
        ret += '        <tr>'
        ret += '            <td><strong>Nombre</strong></td>'
        ret += '            <td><strong>Deuda</strong></td>'
        ret += '            <td><strong>Observaciones</strong></td>'
        ret += '        </tr>'

        for dict in data:
            for alumna in dict['alumnas']:
                if self.missing_data(alumna) or alumna.partner_id.credit != 0:
                    ret += '<tr>'
                    ret += '    <td>' + alumna.partner_id.name + '</td>'
                    ret += '    <td>' + str(alumna.partner_id.credit) + '</td>'
                    ret += '    <td>' + self.missing_data(alumna) + '</td>'
                    ret += '</tr>'

        ret += '    </tbody>'
        ret += '</table>'

        return ret

    def button_generate_daily_report(self):
        # Obtener la fecha para el reporte
        for reg in self:
            date = reg.date

        data = []
        # Obtener todas las clases de la fecha del reporte solo para cursos confirmados.
        lectures = []
        for lecture in self.env['curso.lecture'].search([('date', '=', date)]):
            if lecture.curso_id.state == 'confirm':
                lectures.append(lecture)

        # por cada clase obtener todas las alumnas en estado confirmado o señado
        pool_reg = self.pool.get('curso.registration')
        for lecture in lectures:
            alumnas = []
            alumnas = pool_reg.search([('curso_id', '=', lecture.curso_id.id),
                                       ('state', 'in', ['confirm', 'signed'])])
            for alumna in alumnas:
                alumnas.append(alumna)

            data.append(
                    {'curso': lecture.curso_id.name,
                     'tema': lecture.name or 'Clase no definida',
                     'alumnas': alumnas
                     }
            )

        report_name = "Reporte Diario " + datetime.strftime(
                datetime.strptime(date, '%Y-%m-%d'), '%d/%m/%Y')

        new_page = {
            'name': report_name,
            'content': self.generate_local_html(data),
        }

        # Borrar el documento si es que existe
        doc_pool = self.env['document.page']
        document = doc_pool.search([('name', '=', report_name)])
        document.unlink()

        # Generar el documento
        self.env['document.page'].create(new_page)

        return True


#    _columns = {
#        'date': fields.date('Fecha', required=True,
#                            help=u"La fecha para la que se va a generar el reporte"),
#    }
