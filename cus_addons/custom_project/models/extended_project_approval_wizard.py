from odoo import models, fields, api
import datetime
# در سرور با دستور زیر نصب شد 
#PS E:\software setup\Odoo18\server> ..\python\python.exe -m pip install jdatetime
import jdatetime

class ProjectApprovalWizardExtended(models.TransientModel):
    _name = 'project.approval.wizard.extended'
    _description = 'پاپ آپ تصویب پروژه'

    project_id = fields.Many2one('project.project', string='پروژه', required=True) # foreign key
    x_approval_code = fields.Char(string='کد تصویب', related='project_id.x_approval_code', readonly=False, export_string_translation=False) # this field related to 'x_approval_code' that declare in 'extended_project.py', this field is foreign key of 'x_approval_code' in 'extended_project.py'
    
    # def confirm_approvalcode(self):
    #     if not self.x_approval_code:
    #         company_id = self.project_id.company_id 
    #         if company_id:
    #             if company_id.x_company_system_code_id:
    #                 self.x_approval_code = "404" + "_" + self.project_id.id company_id.x_company_system_code_id
    #                 return {'type': 'ir.actions.act_window_close'}        
    #             else :
    #                 self.project_id.message_post(body="سیستم کد مرکز ثبت نشده است")
    #                 return {
    #                     'type': 'ir.actions.client',
    #                     'tag': 'display_notification',
    #                     'params': {
    #                         'type': 'danger',  # 'danger' for error, 'warning' for a warning message
    #                         'title': 'خطا',
    #                         'message': 'سیستم کد مرکز ثبت نشده است.',
    #                         'sticky': False,
    #                     }
    #                 }
    #         else :
    #             self.project_id.message_post(body="شناسه شرکت برای پروژه یافت نشد")
    #             return {
    #                 'type': 'ir.actions.client',
    #                 'tag': 'display_notification',
    #                 'params': {
    #                     'type': 'danger',     # 'danger' for error, 'warning' for a warning message
    #                     'title': 'خطا',
    #                     'message': 'شناسه شرکت برای پروژه یافت نشد.',
    #                     'sticky': False,
    #                 }
    #             }
            
    #     #self.x_approval_code = 123  # or use random string generation like this: ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    #     #return {'type': 'ir.actions.act_window_close'}
        
        
        
    def confirm_approvalcode(self):
        if not self.x_approval_code:
            jalali_date = jdatetime.date.fromgregorian(date=self.create_date.date())
            jalali_year = jalali_date.year #1404
            jalaliYear_lastThreeDigits = str(jalali_year)[-3:] # 404
            self.x_approval_code = jalaliYear_lastThreeDigits + str(self.project_id.id) #for example : 404_110  #سه رقم آخر سال شمسی_شناسه پروژه
            return {'type': 'ir.actions.act_window_close'}
        else: 
            return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'type': 'warning',     # 'danger' for error, 'warning' for a warning message
                        'title': 'هشدار',
                        'message': 'این پروژه قبلا تصویب شده است',
                        'sticky': False,
                    }
                }