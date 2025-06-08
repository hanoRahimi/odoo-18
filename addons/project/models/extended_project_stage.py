from odoo import models, fields, api

import logging 
_logger = logging.getLogger(__name__)

class ProjectStageExtended(models.Model):
    _inherit = 'project.project.stage'

    x_stage_max_inprogress_percentage = fields.Float(string='ماکزیمم درصد پیشرفت برای استیج مربوطه', store=True, readonly=False) #, compute='_onchange_stage_max_inprogress_percentage'
    #x_stage_importance_number = fields.Float(string='اهمیت جایگاه', store=True, readonly=False) # in this time not used

    # جایگذاری پروژه ها بر اساس درصد پیشرفت روی stage ها، زمانی که وزن stage تغییر می کند
    @api.onchange('x_stage_max_inprogress_percentage')
    def _onchange_stage_max_inprogress_percentage(self): 
        _logger.info('▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄ _onchange_stage_max_inprogress_percentage ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄')
        myStages = self.env['project.project.stage'].search([], order='x_stage_max_inprogress_percentage asc')  
    
        for stage in self: 
            my_stage = next((s for s in myStages if "NewId_" + str(s.id) == str(self.id)), None) # self id format => NewId_14
            if my_stage: 
                my_stage.x_stage_max_inprogress_percentage = stage.x_stage_max_inprogress_percentage

        projects = self.env['project.project'].search([]) #.search([('stage_id', '=', self.id)])
        projects._reorder_project_Stage(myStages.search([], order='x_stage_max_inprogress_percentage asc'))        


    #def _re_compute_stage_weight():







    # @api.model
    # def write(self, vals):
    #     # ابتدا ذخیره مقدار فیلد در مدل stage
    #     if 'x_stage_max_inprogress_percentage' in vals:
    #         stages = self.filtered(lambda s: 'x_stage_max_inprogress_percentage' in vals)
    #         for stage in stages:
    #             # ذخیره مقدار جدید
    #             stage.x_stage_max_inprogress_percentage = vals['x_stage_max_inprogress_percentage']

    #     # محاسبات پروژه‌ها بلافاصله پس از ذخیره
    #     projects = self.env['project.project'].search([])
    #     projects._compute_inprogress_percentage(doCompute_ProjectInprogressPercentage=False)

    #     # ادامه فرآیند عادی ذخیره
    #     return super().write(vals)

    
    # @api.model # use api.model, for save model before call another _compute_inprogress_percentage function in extended_project.py
    # def _store_stage_values_to_database(self): 
    #     #self.env['project.project.stage'].write({'x_stage_max_inprogress_percentage': self.x_stage_max_inprogress_percentage})
    #     #self.write({'x_stage_max_inprogress_percentage': self.x_stage_max_inprogress_percentage}) 
    #     #self.env['project.project.stage'].browse(self.id).write({'x_stage_max_inprogress_percentage': self.x_stage_max_inprogress_percentage})
    #     #self.env.cr.commit()
        
    #     # جستجوی رکورد stage مرتبط با مقدار self.id
    #     stage = self.env['project.project.stage'].browse(self.id)
    #     # ذخیره مقدار در پایگاه داده
    #     stage.write({'x_stage_max_inprogress_percentage': self.x_stage_max_inprogress_percentage})
    #     # اطمینان از ذخیره‌سازی (با استفاده از _flush)
    #     self.env['project.project.stage']._flush(['x_stage_max_inprogress_percentage'])
        