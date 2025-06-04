from odoo import http
from odoo.http import request, Response
import json
import re

class ProjectAPIController(http.Controller):
    
    # ----------------  پروژه -----------------
    @http.route('/api/projects', auth='user', type='json', csrf=False, methods=['POST'])
    def get_projects(self, **kwargs):
        def clean_html(raw_html):
            clean_text = re.sub('<[^<]+?>', '', raw_html or "")
            return clean_text.strip()

        projects = request.env['project.project'].sudo().search([])
        data = []
        for project in projects:
            data.append({
                'id': project.id,
                'name': project.name,
                'create_date': str(project.create_date),
                'date_start_schedule': str(project.date_start),
                'date_end_schedule': str(project.date),
                'description': clean_html(project.description),
                'progres_actual': project.task_completion_percentage,
                'approval_code': project.x_approval_code,
                'budget': project.budget,
                'company': project.partner_id.name,
                'tags': [tag.name for tag in project.tag_ids],
                'user_id': project.user_id.id,
                'user_name': project.user_id.name,
            })
        return data


    # -------------- فعالیت‌های پروژه ---------------
    @http.route('/api/activities', auth='user', methods=['POST'], type='json', csrf=False)
    def get_activities(self, **kwargs):
        activity_task = request.env['project.task'].sudo().search([])
        result = []
        for task in activity_task:
            result.append({
                'id': task.id,
                'name': task.name,
                'project_id': task.project_id.id,
                'project_name': task.project_id.name,
                'date_deadline': str(task.date_deadline) if task.date_deadline else None,
                'user_ids': task.user_ids.ids,
                'tag_ids': [tag.name for tag in task.tag_ids],
                'start_date_schedule': str(task.x_scheduled_start_date) if task.x_scheduled_start_date else None,
                'end_date_schedule': str(task.x_scheduled_end_date) if task.x_scheduled_end_date else None,
                'start_date_actual': str(task.x_actual_start_date) if task.x_actual_start_date else None,
                'end_date_actual': str(task.x_actual_end_date) if task.x_actual_end_date else None,
                'progres': task.x_activity_progress,
                'budget': task.x_budget_ceiling,
            })
        return result

    # -------------- زیر وظایف (Task) ---------------
    @http.route('/api/subtasks', auth='user', methods=['POST'], type='json', csrf=False)
    def get_subtasks(self, **kwargs):
        subtasks = request.env['project.task'].search([('parent_id', '!=', False)])
        result = []
        for sub in subtasks:
            result.append({
                'id': sub.id,
                'name': sub.name,
                'deadline': sub.date_deadline,
                'project_parent_id': sub.parent_id.id,
                'project_parent_name': sub.parent_id.name,
                'user_id': sub.user_ids.ids,
                'tags': [tag.name for tag in sub.tag_ids],
            })
        return result

    # -------------- کاربران ---------------
    @http.route('/api/users', auth='user', type='json', methods=['POST'], csrf=False)
    def get_users(self, **kwargs):
        users = request.env['res.users'].sudo().search([])
        result = []
        for u in users:
            result.append({
                'name': u.name,
                'id': u.id,
                'login': u.login,
                'company_id': u.company_id.id if u.company_id else False,
                'email': u.email,
            })
        return result





    