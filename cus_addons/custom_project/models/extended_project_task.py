from odoo import models, fields, api
import jdatetime
import logging
from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)


class Project_task_Extended(models.Model):
    _inherit = 'project.task'
    # _name = 'project.task'

    x_scheduled_start_date = fields.Date(string='تاریخ شروع برنامه ای')
    x_scheduled_end_date = fields.Date(string='تاریخ پایان برنامه ای')
    X_scheduled_duration = fields.Integer(string='مدت زمان برنامه ای (روز)', export_string_translation=True, readonly=True, compute='_compute_scheduled_duration')

    x_actual_start_date = fields.Date(string='تاریخ شروع واقعی')
    x_actual_end_date = fields.Date(string='تاریخ پایان واقعی')
    X_actual_duration = fields.Integer(string='مدت زمان واقعی (روز)', export_string_translation=True, readonly=True, compute='_compute_actual_duration')

    #x_studio_budget_ceiling = fields.Monetary(string='بودجه برنامه ریزی شده', related="account_id.balance")
    x_budget_ceiling = fields.Monetary(string='بودجه برنامه ریزی شده', currency_field='x_currency_id') #Budget Ceiling
    x_currency_id = fields.Many2one('res.currency', string='واحد پول')

    x_deliverableItem = fields.Html('اقلام قابل تحویل', help="اقلام قابل تحویل را وارد نمایید")
    # x_deliverableItem = fields.Char('اقلام قابل تحویل', export_string_translation=True)

    x_activity_progress = fields.Selection([
        ('0', '0%'),
        ('10', '10%'),
        ('20', '20%'),
        ('30', '30%'),
        ('40', '40%'),
        ('50', '50%'),
        ('60', '60%'),
        ('70', '70%'),
        ('80', '80%'),
        ('90', '90%'),
        ('100', '100%')], 
        'پیشرفت فعالیت', required=True, default='0')


    @api.constrains('x_scheduled_start_date', 'x_scheduled_end_date', 'parent_id')
    def _check_task_dates_within_project(self):
        for task in self:
            if not task.project_id:
                continue

            project = task.project_id

            if project.date_start and task.x_scheduled_start_date:
                if task.x_scheduled_start_date < project.date_start:
                    raise UserError("تاریخ شروع فعالیت نباید از تاریخ شروع پروژه کمتر باشد.")

            if project.date and task.x_scheduled_end_date:
                if task.x_scheduled_end_date > project.date:
                    raise UserError("تاریخ پایان فعالیت نباید از تاریخ پایان پروژه بیشتر باشد.")


    #@api.onchange('x_importance')
    @api.depends('x_scheduled_start_date', 'x_scheduled_end_date')
    def _compute_scheduled_duration(self):
        for projetActivityRecord in self: # once execute
            if all([projetActivityRecord.x_scheduled_start_date, projetActivityRecord.x_scheduled_end_date]) : # if has value together   #projetActivityRecord.x_scheduled_start_date is not None and projetActivityRecord.x_scheduled_end_date is not None:
                if projetActivityRecord.x_scheduled_end_date>projetActivityRecord.x_scheduled_start_date :
                    projetActivityRecord.X_scheduled_duration = (projetActivityRecord.x_scheduled_end_date - projetActivityRecord.x_scheduled_start_date).days + 1
                else:
                    projetActivityRecord.X_scheduled_duration = 0
            else:
                projetActivityRecord.X_scheduled_duration = 0

        # set 'nearest' and 'farthest' project task 'scheduled_start_date' and 'scheduled_end_date' to project record => 'date_start','date' field for scheduled_date
        # project_id = projetActivityRecord.project_id.id if projetActivityRecord.project_id else None
        # if projetActivityRecord.project_id:
        nearest_scheduled_start_date = self.env['project.task'].search([
                                                        ('project_id', '=', projetActivityRecord.project_id.id),
                                                        ('x_scheduled_start_date', '!=', False)
                                                        ], order='x_scheduled_start_date asc', limit=1)
        
        farthest_scheduled_end_date = self.env['project.task'].search([
                                                        ('project_id', '=', projetActivityRecord.project_id.id),
                                                        ('x_scheduled_end_date', '!=', False)
                                                        ], order='x_scheduled_end_date desc', limit=1)

        if nearest_scheduled_start_date:
            projetActivityRecord.project_id.date_start = nearest_scheduled_start_date.x_scheduled_start_date
        
        if farthest_scheduled_end_date:
            projetActivityRecord.project_id.date = farthest_scheduled_end_date.x_scheduled_end_date
        



    @api.depends('x_actual_start_date', 'x_actual_end_date')
    def _compute_actual_duration(self):
        for projetActivityRecord in self: # once execute
            if all([projetActivityRecord.x_actual_start_date, projetActivityRecord.x_actual_end_date]) : # if has value together  #if projetActivityRecord.x_actual_start_date is not None and projetActivityRecord.x_actual_end_date is not None:
                if projetActivityRecord.x_actual_end_date>projetActivityRecord.x_actual_start_date :
                    projetActivityRecord.X_actual_duration = (projetActivityRecord.x_actual_end_date - projetActivityRecord.x_actual_start_date).days + 1
                else:
                    projetActivityRecord.X_actual_duration = 0
            else:
                projetActivityRecord.X_actual_duration = 0

                