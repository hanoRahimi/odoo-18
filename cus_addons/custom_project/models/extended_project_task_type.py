from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)
#_logger.setLevel(logging.DEBUG)  # برای اطمینان از ثبت پیام‌های DEBUG و INFO


class Project_task_type_Extended(models.Model):
    _inherit = 'project.task.type'
    # _name = 'project.task.type'

    x_importance = fields.Float(string='Importance', store=True, default=100)
    x_weight = fields.Float(string='Weight', store=True, default=100) #, compute='_compute_weight_per_percentage'

    
    #@api.onchange('x_importance')
    # @api.depends('x_importance')
    # def _compute_weight_per_percentage(self):
    #     _logger.info('▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄ start ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄')
    #     for record in self:
    #         record.x_weight = record.x_importance / 100



    # x_importance = fields.Float(string='Importance', store=True, default=100) # میزان اهمیت $ project task type weight importance, set free number, ex: 80, 1000, 5, ..., after calculate "weight" percentage field by "importance" field
    # x_weight = fields.Float(string='Weight', store=True, default=100) #compute='_compute_weight_per_percentage'  #project task type weight by percentage, automatic calculated

    # @api.depends('x_importance')
    # def _compute_weight_per_percentage(self):
    #     _logger.error("▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄ salam2 ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄")
    #     #_logger.info('▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄ salam2 ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄')
    #     for record in self:
    #         _logger.error('▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄ start ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄ ')            
    #         record.x_weight = record.x_importance / 10

    #         #project_id = self.project_ids.id if self.project_ids else None # is many to many field
    #         # project_id = record.project_ids.id
    #         # _logger.info('▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄ project_id : %s', project_id)



    # محاسبه وزن هر stage یا task type
    # x_importance => model : project.task.type
    # formula : 
    # x_weight = ((x_importance * 100) / sum(total_importance)) وزن هر یک از stage فعالیت ها

    # بدست آوردن تمامی وزن های استیج فعالیت های مربوط به پروژه مربوطه
    # 1. دریافت شناسه پروژه
    # 2. دریافت وزن تمامی فعالیت های پروژه
    # 3. محاسبه فرمول تمامی استیج ها بر اساس x_importance و سپس ذخیره وزن هر استیج روی x_weight
    # 4. با تغییر x_weight توابع محاسبه درصد پیشرفت پروژه به صورت خودکار صدا زده می شود و درصد پیشرفت پروژه را بر اساس تغییرات وزن استیج فعالیت ها عوض می کند
    # @api.depends('x_importance')
    # def _compute_weight_per_percentage(self):
    #     #first_task_type = self #self.env['project.task.type'].search([], limit=1)
    #     _logger.info('▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄ start : ')
    #     #project_id = self.project_ids.id
    #     project_id = self.project_ids.id if self.project_ids else None # is many to many field

    #     _logger.info('▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄ project_id : ' + project_id)
    #     if project_id:
    #         _logger.info('▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄ start : ')
    #         #taskTypes = self.env['project.task.type'].search([('project_id', '=', project_id)], order='x_stage_max_inprogress_percentage asc')
    #         taskTypes = self.env['project.task.type'].search([('project_ids', 'in', [project_id])])
    #         _logger.info('▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄ task type record len : ' + len(taskTypes))
    #         total_importance = sum(taskTypes.mapped('x_importance'))
    #         _logger.info('▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄ total_importance : ' + total_importance)

    #         for taskType in taskTypes: 
    #             my_taskType = next((t for t in taskType if "NewId_" + str(t.project_ids.id) == str(project_id)), None)
    #             if my_taskType: 
    #                 my_taskType.x_weight = ((my_taskType.x_importance * 100) / sum(total_importance))
    #                 _logger.info('▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄ my_taskType.x_weight : ' + my_taskType.x_weight)

    #         # projects = self.env['project.project'].search([('id', '=', project_id)]) # self.env['project.project'].search([])
    #         # projects._reorder_project_Stage(taskType.search([], order='x_stage_max_inprogress_percentage asc'))      


    # این تابع برای ایجاد stage های پروژه به صورت پیش فرض هنگامی که پروژه ایجاد می شود نوشته شده است
    @api.model
    def _CreateProjectTaskType(self, projects):
        #project_pigs = self.env['project.project'].search([('name', '=', 'testProj1')]) #self.name #Pigs #'دیوار مهربانی'
        for project in projects:
            # (4, id): فقط یک پروژه موجود را اضافه می‌کند (بدون حذف پروژه‌های قبلی).
            # (6, 0, [ids]): همه‌ی پروژه‌های قبلی را حذف کرده و پروژه‌های جدید را اضافه می‌کند.
            # مثال: حذف رابطه‌ی یک project از stage بدون حذف پروژه از دیتابیس
            # - ارتباط بین stage_a و پروژه‌ای با id=10 قطع می‌شود، اما پروژه همچنان در دیتابیس باقی می‌ماند.
                # stage_a = self.env['project.task.type'].create({
                #     'name': 'a',
                #     'project_ids': [(3, 10)]
                # })
            #اضافه کردن رابطه با یک رکورد موجود
            # stage_a = self.env['project.task.type'].create({
            #     'name': 'a',
            #     'project_ids': [(4, project.id)]
            # })
            # , ...

            # project_ids is many2many type and 4 means add record to current exist project
            # stage_a = self.env['project.task.type'].create({'name': 'مطالعات امکان سنجی', 'project_ids': [(4, project.id)], 'x_weight': 25})
            # stage_b = self.env['project.task.type'].create({'name': 'برنامه ریزی پروژه', 'project_ids': [(4, project.id)], 'x_weight': 25})
            # stage_c = self.env['project.task.type'].create({'name': 'انجام پروژه', 'project_ids': [(4, project.id)], 'x_weight': 25})
            # stage_d = self.env['project.task.type'].create({'name': 'تحویل پروژه', 'project_ids': [(4, project.id)], 'x_weight': 25})
            stage_a = self.env['project.task.type'].create({'name': 'سه ماهه اول', 'project_ids': [(4, project.id)], 'x_weight': 25})
            stage_b = self.env['project.task.type'].create({'name': 'سه ماهه دوم', 'project_ids': [(4, project.id)], 'x_weight': 25})
            stage_c = self.env['project.task.type'].create({'name': 'سه ماهه سوم', 'project_ids': [(4, project.id)], 'x_weight': 25})
            stage_d = self.env['project.task.type'].create({'name': 'سه ماهه چهارم', 'project_ids': [(4, project.id)], 'x_weight': 25})

            # stage_a = self.env['project.task.type'].create({
            #     'name': 'a',
            #     'project_ids': [(0, 0, {'id': project.id})] # دقت کنید که اگر فقط id را بخواهید، معمولاً استفاده از (4, id) مناسب است.
            # })

            task = self.env['project.task'].with_context({
                'default_state': '04_waiting_normal', #04_waiting_normal # default_state
            }).create({
                'name': 'فعالیت من',
                'project_id': project.id #project_pigs.id,
            })
            # self.assertEqual(task.state, '01_in_progress', "The task should be in progress")