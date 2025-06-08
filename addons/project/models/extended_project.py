from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
#_logger.setLevel(logging.DEBUG)
#_logger.setLevel(logging.INFO)

import random
import string

class ProjectProjectExtended(models.Model):
    _inherit = 'project.project'

    x_studio_inprogress_percentage_1 = fields.Float(string='Project In Progress Percentage', compute='_compute_inprogress_percentage', store=True)
    #last_update_status = fields.Selection([('on_track', 'On Track'), ('off_track', 'Off Track')], string='Last Update Status')

    x_approval_code =fields.Char(string='کد تصویب', readonly=False, export_string_translation=True) # field that save approval code to it
    display_approvalCode = fields.Char(string='کد تصویب', compute='_compute_display_approvalCode') # compute field, not save to database, for display status in edit project form, display 'x_approval_code' and if not has value display 'تصویب نشده'

    #▄ محاسبه پیشرفت پروژه
    # task_ids.x_activity_progress => model : project.task
    # task_ids.stage_id.x_weight => model : project.task.type
    # last_update_status => model : project
    @api.depends('task_ids.x_activity_progress', 'task_ids.stage_id.x_weight', 'last_update_status')
    def _compute_inprogress_percentage(self):
        #_logger.info('▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄ start ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄')
        #_logger.debug('▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄ start ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄')
        for project in self:
            total_percentage = 0
            #total_weight = 0
            for stage in project.task_ids.mapped('stage_id'):
                stage_tasks = project.task_ids.filtered(lambda t: t.stage_id == stage)
                if stage_tasks:
                    stage_weight = stage.x_weight
                    activity_progress_sum = sum(float(task.x_activity_progress) for task in stage_tasks)
                    stage_percentage = (activity_progress_sum / len(stage_tasks)) * (stage_weight / 100)
                    total_percentage += stage_percentage
                    #total_weight += stage_weight
            project.x_studio_inprogress_percentage_1 = total_percentage

        stages = self.env['project.project.stage'].search([], order='x_stage_max_inprogress_percentage asc')  
        self._reorder_project_Stage(stages) #self.env['project.project.stage']._reorder_project_Stage(projects:self)


    #▄ تعیین دوباره جایگاه پروژه ها در استیج ها
    def _reorder_project_Stage(self,stages): #_reorder_project_Stage(self, 
        for project in self:
            if project.last_update_status == 'off_track':
                stage = next((s for s in stages if s.x_stage_max_inprogress_percentage == -1), None)
                project.stage_id = stage.id
            else:
                # پیدا کردن اولین مرحله‌ای که مقدار x_stage_max_inprogress_percentage آن بزرگتر از x_studio_inprogress_percentage_1 است 
                stage = next((s for s in stages if s.x_stage_max_inprogress_percentage >= project.x_studio_inprogress_percentage_1), None) 
                project.stage_id = stage.id
                

    #▄ open approvalcode_popup when click on 'تصویب پروژه' in project edit form -> extended_project_views.xml -> extended_edit_project 
    def action_show_approvalcode_popup(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'تصویب پروژه',
            'res_model': 'project.approval.wizard.extended',
            'view_mode': 'form',
             #'views': [(self.env.ref('project.view_project_approvalcode_confirm').id, 'form')],
             #'views': 'form', #[(False, 'form')],
            'target': 'new',
            'context': {'default_project_id': self.id}, #'context': {'default_kip': ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)) if not self.x_approval_code else self.x_approval_code}
        }
        
    #▄
    def _compute_display_approvalCode(self):
        for record in self:
            record.display_approvalCode = record.x_approval_code or "تصویب نشده"