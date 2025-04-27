from odoo import fields, models

class Project(models.Model):
    _inherit = 'project.project'

    partner_id = fields.Many2one('res.partner', string='شرکت', auto_join=True, tracking=True)
    budget = fields.Integer(string="بودجه لازم")
    # progres = fields.Integer(string="درصد پیشرفت")
    approval_code = fields.Char(string="کد تصویب")
    

    
    def action_project_approval(self):
        pass


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    company_id = fields.Many2one('res.company', string='شرکت')

