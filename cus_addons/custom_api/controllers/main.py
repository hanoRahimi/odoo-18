from odoo import http
from odoo.http import request
import json

# Html Snippets, Gitlens-git supercharged, Html Css Support, Live Server, Lorem ipsum, odoo IDE, Odoo Snippets, Pylance, python, python debugger, rainbow csv, thunder client

class ProjectAPIController(http.Controller):

    @http.route(['/api/projects'], auth='public', type='json', csrf=False)
    def get_projects(self, **kwargs):
        projects = request.env['project.project'].sudo().search([])
        data = []
        for project in projects:
            data.append({
                'name':project.name,
                'create_date': project.create_date,
                'date_start': project.date_start,
                'description': project.description,
                'company': project.partner_id.name,
                'tags':project.tag_ids,
                'approval_code': project.approval_code,
                'user_id': project.user_id.name,

            })
        return data

        # projects = request.env['project.project'].search([])

        # data = []
        # for project in projects:
        #     data.append({
        #         'id': project.id,
        #         'name': project.name,
        #         'user_id': project.user_id.name if project.user_id else None,
        #         'date_start': project.date_start,
        #         'date_end': project.date,
        #         'tasks_count': len(project.task_ids),
        #     })

        # return {
        #     'status': 200,
        #     'message': 'Projects fetched successfully',
        #     'data': data
        # }

    # -------------- فعالیت‌های پروژه ---------------
    @http.route('/api/project_activities', auth='user', methods=['GET'], type='json')
    def get_activities(self, **kwargs):
        activities = request.env['mail.activity'].search([])
        result = []
        for a in activities:
            result.append({
                'id': a.id,
                'summary': a.summary,
                'deadline': a.date_deadline,
                'user_id': a.user_id.id if a.user_id else False,
                'tags': [tag.name for tag in a.tag_ids] if hasattr(a, 'tag_ids') else [],
                'planned_start_date': a.date_deadline, 
                'planned_end_date': a.date_deadline,
                'actual_start_date': None,
                'actual_end_date': None, 
                'progress': None,        
                'planned_budget': None, 
            })
        return result

    # -------------- زیر وظایف (Task) ---------------
    @http.route('/api/subtasks', auth='user', methods=['GET'], type='json')
    def get_subtasks(self, **kwargs):
        subtasks = request.env['project.task'].search([('parent_id', '!=', False)])
        result = []
        for t in subtasks:
            result.append({
                'id': t.id,
                'name': t.name,
                'deadline': t.date_deadline,
                'project_id': t.project_id.id if t.project_id else False,
                'user_id': t.user_id.id if t.user_id else False,
                'tags': [tag.name for tag in t.tag_ids],
            })
        return result

    # -------------- کاربران ---------------
    @http.route('/api/users', auth='user', methods=['GET'], type='json')
    def get_users(self, **kwargs):
        users = request.env['res.users'].search([])
        result = []
        for u in users:
            result.append({
                'id': u.id,
                'name': u.name,
                'login': u.login,
                'company_id': u.company_id.id if u.company_id else False,
                'email': u.email,
            })
        return result
