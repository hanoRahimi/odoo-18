# -*- coding: utf-8 -*-
###############################################################################
{
    'name': 'Customize Login Page Style',
    'version': '18.0.1.0.0',
    'category': 'Extra Tools',
    'summary': 'Customize The Login Page',
    'description': 'The Module helps to customize login page with different '
                   'styles',
    'author': '',
    'company': '',
    'maintainer': '',
    'website': '',
    'depends': ['base','base_setup','web'],
    'data': [
        'views/res_config_settings_views.xml',
        'views/webclient_templates_right.xml',
        'views/webclient_templates_left.xml',
        'views/webclient_templates_middle.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'web_login_styles/static/src/scss/custom_style.scss',
            # 'web_login_styles/views/navbar_inherit.xml',
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
