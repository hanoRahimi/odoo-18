from odoo import fields, models, api

class Project(models.Model):
    _inherit = 'project.project'

    partner_id = fields.Many2one('res.partner', string='شرکت', auto_join=True, tracking=True)
    budget = fields.Integer(string="بودجه لازم")
    approval_code = fields.Char(string="کد تصویب")
    is_approval_code = fields.Boolean()
    create_date_only = fields.Date(string="Create Date Only", compute="_compute_create_date_only")

    @api.depends('create_date')
    def _compute_create_date_only(self):
        for record in self:
            record.create_date_only = record.create_date and record.create_date.date() or False
    
    def action_project_approval(self):
        pass


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    company_id = fields.Many2one('res.company', string='شرکت')

