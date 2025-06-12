from odoo import fields, models, api

class Project(models.Model):
    _inherit = 'project.project'
    _order = 'create_date desc'

    partner_id = fields.Many2one('res.partner', string='شرکت', auto_join=True, tracking=True)
    budget = fields.Integer(string="بودجه لازم")
    create_date_only = fields.Date(string="Create Date Only", compute="_compute_create_date_only")
    project_resource_description = fields.Html(string="منابع مصرفی پروژه")

    planned_progress = fields.Float(
            string="پیشرفت برنامه‌ای (%)",
            compute='_compute_planned_progress',
            store=True,
            digits=(5, 2),
    )

    stage_id = fields.Many2one('project.project.stage', string='Stage', ondelete='restrict', groups="project.group_project_stages",
        tracking=True, index=True, copy=False, 
        default=lambda self: self.env['project.project.stage'].search([('name', '=', 'شروع نشده')], limit=1),
        group_expand='_read_group_expand_full')

    custodian = fields.Many2one('res.company', string="متولی")

    @api.depends('create_date')
    def _compute_create_date_only(self):
        for record in self:
            record.create_date_only = record.create_date and record.create_date.date() or False

    @api.depends('date_start', 'date')
    def _compute_planned_progress(self):
        today = fields.Date.today()
        for project in self:
            progress = 0

            if project.date_start and project.date:
                start_date = fields.Date.to_date(project.date_start)
                end_date = fields.Date.to_date(project.date)

                if end_date > start_date:
                    total_days = (end_date - start_date).days
                    elapsed_days = (today - start_date).days

                    if today <= start_date:
                        progress = 0
                    elif today >= end_date:
                        progress = 100
                    else:
                        progress = (elapsed_days / total_days)
                else:
                    progress = 0

            project.planned_progress = round(progress, 2)


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    company_id = fields.Many2one('res.company', string='شرکت')

