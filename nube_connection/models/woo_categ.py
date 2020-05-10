# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from openerp import models, fields, api


class CursoWooCateg(models.Model):
    _name = 'curso.woo.categ'

    # esto hace que el name del registro sea path
    _rec_name = 'path'
    _order = 'woo_idx,slug'

    path = fields.Char(
        compute="_compute_path",
        store=True
    )

    nube_id = fields.Integer(
    )

    woo_ids = fields.Char(
        compute="_compute_woo_ids"
    )

    woo_idx = fields.Integer(
        compute="_compute_woo_idx",
        store=True
    )

    slug = fields.Char(
    )

    name = fields.Char(
    )

    parent = fields.Many2one(
        'curso.woo.categ',
        string="Parent"
    )
    published = fields.Boolean(
        'Publicado en tienda nube',
        help=u'Indica si se publica en tienda nube'
    )

    def _path(self):
        for cat in self:
            if cat.parent:
                return u'{} / {} '.format(cat.parent._path(), cat.name)
            else:
                return cat.name

    @api.depends('parent', 'name')
    def _compute_path(self):
        for rec in self:
            rec.path = rec._path()

    def _compute_woo_ids(self):
        for rec in self:
            ids = []
            ids.append(rec.nube_id)
            if rec.parent:
                ids.append(rec.parent.nube_id)
                if rec.parent.parent:
                    ids.append(rec.parent.parent.nube_id)
            rec.woo_ids = ids

    @api.depends('woo_ids')
    def _compute_woo_idx(self):
        for rec in self:
            ids = eval(rec.woo_ids)
            rec.woo_idx = len(ids)
