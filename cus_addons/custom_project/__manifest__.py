# -*- coding: utf-8 -*-

{
    'name': 'Customize Project Module',
    'version': '18.0.1.0.0',
    'category': 'Extra Tools',
    'summary': 'Customize The Base and Project Module Different Styles',
    'description': 'Customize The Base and Project Module Different Styles',
    'author': '',
    'company': '',
    'maintainer': '',
    'website': '',
    'depends': ['base','web', 'project'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/project_project_views.xml',
        'views/project_task_views.xml',
        'views/extended_project_approval_wizard_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'custom_project/static/src/css/project_custom_styles.css',
            'custom_project/static/src/css/form_field_border.css',
            'custom_project/static/src/scss/project_custom_scss.scss',
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}