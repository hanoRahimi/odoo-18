from odoo import api, fields, models


class MenuItem(models.Model):
    _name = 'menu.item'
    _description = "Menu Item"

    name = fields.Char('Menu')
    menu_id = fields.Integer('Menu ID')