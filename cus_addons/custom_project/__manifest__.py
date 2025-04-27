# -*- coding: utf-8 -*-

{
    'name': 'Customize Project Module',
    'version': '18.0.1.0.0',
    'category': 'Extra Tools',
    'summary': 'Customize The Login Page With Different Styles',
    'description': 'The Module helps to customize login page with different '
                   'styles',
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'website': 'https://www.cybrosys.com',
    'depends': ['base','web', 'project'],
    'data': [
        'views/project_project_views.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'custom_project/static/src/css/project_custom_styles.css',
            'custom_project/static/src/scss/project_custom_scss.scss',
        ],
    },
    'images': ['static/description/banner.png'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
