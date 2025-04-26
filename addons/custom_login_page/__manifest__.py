{
    'name': 'Custom Login Theme',
    'version': '1.0',
    'author': 'Your Name',
    'category': 'Themes',
    'depends': ['web'],
    'data': [
        'views/custom_login.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'custom_login_page/static/src/css/login.css',
        ],
    },
    'installable': True,
    'auto_install': False,
}
