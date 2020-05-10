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
    'version': '13.0.0.0',
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

    'limit_request': '8196',
    'limit_memory_soft': '640000000',
    'limit_memory_hard': '760000000',
    'limit_time_cpu': '60',
    'limit_time_real': '120',

    # manifest version, if omitted it is backward compatible
    'env-ver': '2',

    # if Enterprise it installs in a different directory than community
    'odoo-license': 'EE',

    # port where odoo starts serving pages
    'port': '8069',

    # list of url repos to install in the form 'repo-url directory'
    'git-repos': [
        'git@github.com:jobiols/cl-lab.git',
        'https://github.com/OCA/knowledge.git',
#        {'usr': 'jobiols', 'repo': 'odoo-addons', 'branch': '12.0'},
#        {'usr': 'jobiols', 'repo': 'jeo-enterprise', 'branch': '12.0'},

#        {'usr': 'jobiols', 'repo': 'odoo-etl', 'branch': '12.0'},

#        {'usr': 'ingadhoc', 'repo': 'odoo-argentina', 'branch': '12.0'},
#        {'usr': 'ingadhoc', 'repo': 'argentina-sale', 'branch': '12.0'},
#        {'usr': 'ingadhoc', 'repo': 'account-financial-tools',         'branch': '12.0'},
#        {'usr': 'ingadhoc', 'repo': 'account-payment', 'branch': '12.0'},
#        {'usr': 'ingadhoc', 'repo': 'miscellaneous', 'branch': '12.0'},
#        {'usr': 'ingadhoc', 'repo': 'argentina-reporting',         'branch': '12.0'},
#        {'usr': 'ingadhoc', 'repo': 'reporting-engine', 'branch': '12.0'},
#        {'usr': 'ingadhoc', 'repo': 'aeroo_reports', 'branch': '12.0'},
#        {'usr': 'ingadhoc', 'repo': 'sale', 'branch': '12.0'},
#        {'usr': 'ingadhoc', 'repo': 'odoo-support', 'branch': '12.0'},
#        {'usr': 'ingadhoc', 'repo': 'product', 'branch': '12.0'},
#        {'usr': 'ingadhoc', 'repo': 'stock', 'branch': '12.0'},
#        {'usr': 'ingadhoc', 'repo': 'account-invoicing', 'branch': '12.0'},
#        {'usr': 'ingadhoc', 'repo': 'patches', 'branch': '12.0'},

#        {'usr': 'oca', 'repo': 'partner-contact', 'branch': '12.0'},
#        {'usr': 'oca', 'repo': 'web', 'branch': '12.0'},
#        {'usr': 'oca', 'repo': 'server-tools', 'branch': '12.0'},
#        {'usr': 'oca', 'repo': 'social', 'branch': '12.0'},
#        {'usr': 'oca', 'repo': 'server-ux', 'branch': '12.0'},
#        {'usr': 'oca', 'repo': 'server-brand', 'branch': '12.0'},
#        {'usr': 'oca', 'repo': 'manufacture', 'branch': '12.0'},
#        {'usr': 'oca', 'repo': 'manufacture-reporting', 'branch': '12.0'},
#        {'usr': 'oca', 'repo': 'management-system', 'branch': '12.0'},
#        {'usr': 'oca', 'repo': 'sale-workflow', 'branch': '12.0'},
#        {'usr': 'oca', 'repo': 'stock-logistics-warehouse', 'branch': '12.0'},
#        {'usr': 'oca', 'repo': 'stock-logistics-reporting', 'branch': '12.0'},
#        {'usr': 'oca', 'repo': 'stock-logistics-workflow', 'branch': '12.0'},
#        {'usr': 'oca', 'repo': 'queue', 'branch': '12.0'},
#        {'usr': 'oca', 'repo': 'knowledge', 'branch': '12.0'},
    ],

    'docker-images': [
        'odoo jobiols/odoo-ent:13.0e',
        'postgres postgres:10.1-alpine',
        'nginx nginx'
    ]
}
