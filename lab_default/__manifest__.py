# -----------------------------------------------------------------------------
#
#    Copyright (C) 2019  jeo Software  (http://www.jeosoft.com.ar)
#    All Rights Reserved.
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
# -----------------------------------------------------------------------------
{
    'name': 'lab',
    'version': '12.0e.0.0.0',
    'license': 'Other OSI approved licence',
    'category': 'Default Application',
    'summary': 'Customization for lab',
    'author': 'jeo Software',
    'depends': [
        # basic applications
        'sale_management',
        'purchase',
        'stock',

        # minimum modules for argentinian localizacion + utilities + fixes
        'standard_depends_ee',

        # utilitarios
        'mail_tracking_mailgun',

        # 'life' comentamos para que ande travis, esta en privado
    ],
    'data': [
    ],
    'test': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': [],

    # port where odoo starts serving pages
    'port': '8069',
    'repos': [
        {'usr': 'jobiols', 'repo': 'cl-lab', 'branch': '12.0'},
        {'usr': 'jobiols', 'repo': 'odoo-addons', 'branch': '12.0'},
        {'usr': 'jobiols', 'repo': 'jeo-enterprise', 'branch': '12.0',
         'ssh': True, 'host': 'bitbucket.org'},

        {'usr': 'jobiols', 'repo': 'odoo-etl', 'branch': '12.0'},

        {'usr': 'ingadhoc', 'repo': 'odoo-argentina', 'branch': '12.0'},
        {'usr': 'ingadhoc', 'repo': 'argentina-sale', 'branch': '12.0'},
        {'usr': 'ingadhoc', 'repo': 'account-financial-tools',
         'branch': '12.0'},
        {'usr': 'ingadhoc', 'repo': 'account-payment', 'branch': '12.0'},
        {'usr': 'ingadhoc', 'repo': 'miscellaneous', 'branch': '12.0'},
        {'usr': 'ingadhoc', 'repo': 'argentina-reporting',
         'branch': '12.0'},
        {'usr': 'ingadhoc', 'repo': 'reporting-engine', 'branch': '12.0'},
        {'usr': 'ingadhoc', 'repo': 'aeroo_reports', 'branch': '12.0'},
        {'usr': 'ingadhoc', 'repo': 'sale', 'branch': '12.0'},
        {'usr': 'ingadhoc', 'repo': 'odoo-support', 'branch': '12.0'},
        {'usr': 'ingadhoc', 'repo': 'product', 'branch': '12.0'},
        {'usr': 'ingadhoc', 'repo': 'stock', 'branch': '12.0'},
        {'usr': 'ingadhoc', 'repo': 'account-invoicing', 'branch': '12.0'},
        {'usr': 'ingadhoc', 'repo': 'patches', 'branch': '12.0'},

        {'usr': 'oca', 'repo': 'partner-contact', 'branch': '12.0'},
        {'usr': 'oca', 'repo': 'web', 'branch': '12.0'},
        {'usr': 'oca', 'repo': 'server-tools', 'branch': '12.0'},
        {'usr': 'oca', 'repo': 'social', 'branch': '12.0'},
        {'usr': 'oca', 'repo': 'server-ux', 'branch': '12.0'},
        {'usr': 'oca', 'repo': 'server-brand', 'branch': '12.0'},
        {'usr': 'oca', 'repo': 'manufacture', 'branch': '12.0'},
        {'usr': 'oca', 'repo': 'manufacture-reporting', 'branch': '12.0'},
        {'usr': 'oca', 'repo': 'management-system', 'branch': '12.0'},
        {'usr': 'oca', 'repo': 'sale-workflow', 'branch': '12.0'},
        {'usr': 'oca', 'repo': 'stock-logistics-warehouse', 'branch': '12.0'},
        {'usr': 'oca', 'repo': 'stock-logistics-reporting', 'branch': '12.0'},
        {'usr': 'oca', 'repo': 'stock-logistics-workflow', 'branch': '12.0'},
        {'usr': 'oca', 'repo': 'queue', 'branch': '12.0'},
        {'usr': 'oca', 'repo': 'knowledge', 'branch': '12.0'},
    ],

    # example images version 1
    'docker': [
        {'name': 'odoo', 'usr': 'jobiols', 'img': 'odoo-ent', 'ver': '12.0e'},
        {'name': 'postgres', 'usr': 'postgres', 'ver': '10.1-alpine'},
        {'name': 'nginx', 'usr': 'nginx', 'ver': 'latest'},
        {'name': 'aeroo', 'usr': 'adhoc', 'img': 'aeroo-docs'},
    ],
}
