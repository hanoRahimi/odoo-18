from odoo import http
from odoo.http import request

class CustomLoginPage(http.Controller):
    @http.route('/web/login', type='http', auth="public", website=True)
    def login(self, **kw):
        return request.render('custom_login_page.custom_login_template')
