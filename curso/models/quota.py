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


class curso_quota(models.Model):
    _name = 'curso.quota'
    _order = 'date desc'

    registration_id = fields.Many2one(
        'curso.registration',
        'Inscripcion',
        required=True
    )

    date = fields.Date(
        'Fecha factura'
    )

    list_price = fields.Float(
        'Precio'
    )

    quota = fields.Integer(
        '#cuota',
        readonly=False
    )

    invoice_id = fields.Many2one(
        'account.invoice',
        'Factura',
        required=False
    )

    amount = fields.Char(
        compute="_compute_amount",
        string='Facturado'
    )

    state = fields.Char(
        compute="_get_state",
        string='Estado Factura'
    )

    curso_inst = fields.Char(
        related='registration_id.curso_id.curso_instance',
        string='Instancia',
        readonly=True
    )

    partner_id = fields.Char(
        related='registration_id.partner_id.name',
        string='Alumna',
        readonly=True
    )

    def _get_state(self):
        for rec in self:
            rec.state = 'Pendiente'
            if rec.invoice_id:
                account_invoice_obj = rec.env['account.invoice']
                domain = [('id', '=', rec.invoice_id.id)]
                for invoice in account_invoice_obj.search(domain):
                    if invoice.state == 'draft':
                        rec.state = 'Borrador'
                    if invoice.state == 'paid':
                        rec.state = 'Pagado'
                    if invoice.state == 'open':
                        rec.state = 'Abierto'
                    if invoice.state == 'cancel':
                        rec.state = 'Cancelado'

    def _compute_amount(self):
        for rec in self:
            rec.amount = 0
            if rec.invoice_id:
                account_invoice_obj = self.env['account.invoice']
                domain = [('id', '=', rec.invoice_id.id)]
                for invoice in account_invoice_obj.search(domain):
                    rec.amount = invoice.amount_total
