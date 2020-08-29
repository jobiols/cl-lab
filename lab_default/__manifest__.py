# -----------------------------------------------------------------------------
#
#    Copyright (C) 2020  jeo Software  (http://www.jeosoft.com.ar)
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
        'https://github.com/jobiols/cl-lab.git',
        'git@github.com:jobiols/jeo-enterprise.git',

        # contiene standard depends
        'https://github.com/jobiols/odoo-addons.git',

        # Adhoc para localizacion
        'https://github.com/ingadhoc/odoo-argentina.git',
        'https://github.com/ingadhoc/miscellaneous',
        'https://github.com/ingadhoc/account-financial-tools',
        'https://github.com/ingadhoc/sale',
        'https://github.com/ingadhoc/product',
        'https://github.com/ingadhoc/argentina-sale',
        'https://github.com/ingadhoc/account-payment',
        'https://github.com/ingadhoc/stock',

        # oca para localizacion
        'https://github.com/oca/web',

        # otros repositorios adicionales ADHOC
        ###########################################################
        'https://github.com/ingadhoc/website',
        'https://github.com/ingadhoc/partner',
        'https://github.com/ingadhoc/account-invoicing',

        # otros repositorios adicionales OCA
        ###########################################################
        'https://github.com/oca/partner-contact',
        'https://github.com/oca/sale-workflow',
        'https://github.com/oca/server-ux',
        'https://github.com/oca/contract',
        'https://github.com/oca/stock-logistics-workflow.git',
    ],

    'docker-images': [
        'odoo jobiols/odoo-ent:13.0e',
        'postgres postgres:10.1-alpine',
        'nginx nginx'
    ]
}
