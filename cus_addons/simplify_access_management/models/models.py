from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, AccessError
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval
from odoo.addons.advanced_web_domain_widget.models.domain_prepare import prepare_domain_v2,compute_domain
from odoo.tools.sql import SQL
from .query_prepare import search_data



class BaseModel(models.AbstractModel):
    _inherit = 'base'

    @api.model
    def get_views(self, views, options=None):
        res = super().get_views(views, options)
        form_toolbar = res['views'].get('form', {}).get('toolbar') or False
        tree_toolbar = res['views'].get('list', {}).get('toolbar') or False
        # remove_action = self.env['remove.action'].sudo().search(
        #     [('access_management_id.active', '=', True),
        #      ('access_management_id', 'in', self.env.user.access_management_ids.ids),
        #      ('model_id.model', '=', self._name)])
        
        # remove_action -= remove_action.filtered(lambda x: x.access_management_id.is_apply_on_without_company == False and self.env.company.id not in x.access_management_id.company_ids.ids)
        remove_action = search_data(self, 'remove.action', search_model=self._name)
        if remove_action:
            if form_toolbar or tree_toolbar:
                remove_server_action = remove_action.mapped('server_action_ids.action_id').ids
                remove_print_action = remove_action.mapped('report_action_ids.action_id').ids
            if form_toolbar:
                if res['views']['form']['toolbar'].get('action', False):
                    action = [rec for rec in res['views']['form']['toolbar']['action'] if
                            rec.get('id', False) not in remove_server_action]
                    res['views']['form']['toolbar']['action'] = action
                if res['views']['form']['toolbar'].get('print', False):
                    prints = [rec for rec in res['views']['form']['toolbar']['print'] if
                            rec.get('id', False) not in remove_print_action]
                    res['views']['form']['toolbar']['print'] = prints
            if tree_toolbar:
                if res['views']['list']['toolbar'].get('action', False):
                    action = [rec for rec in res['views']['list']['toolbar']['action'] if
                            rec.get('id', False) not in remove_server_action]
                    res['views']['list']['toolbar']['action'] = action
                if res['views']['list']['toolbar'].get('print', False):
                    prints = [rec for rec in res['views']['list']['toolbar']['print'] if
                            rec.get('id', False) not in remove_print_action]
                    res['views']['list']['toolbar']['print'] = prints
      
        return res

    @api.model
    def load_views(self, views, options=None):
        actions_and_prints = []
        # remove_action = self.env['remove.action'].sudo().search([('access_management_id.active', '=', True),
        #                                         ('access_management_id', 'in',self.env.user.access_management_ids.ids),
        #                                         ('model_id.model', '=', self._name)])
        # remove_action -= remove_action.filtered(lambda x: x.access_management_id.is_apply_on_without_company == False and self.env.company.id not in x.access_management_id.company_ids.ids)
        remove_action = search_data(self, 'remove.action', search_model=self._name)
        for access in remove_action:
            actions_and_prints = actions_and_prints + access.mapped('report_action_ids.action_id').ids
            actions_and_prints = actions_and_prints + access.mapped('server_action_ids.action_id').ids
            for view_data in access.view_data_ids:
                for view_data_list in views:
                    if view_data.techname == view_data_list[1]:
                        views.pop(views.index(view_data_list))

        res = super(BaseModel, self).load_views(views, options=options)

        if 'fields_views' in res.keys():
            for view in ['list', 'form']:
                if view in res['fields_views'].keys():
                    if 'toolbar' in res['fields_views'][view].keys():
                        if 'print' in res['fields_views'][view]['toolbar'].keys():
                            prints = res['fields_views'][view]['toolbar']['print'][:]
                            for pri in prints:
                                if pri['id'] in actions_and_prints:
                                    res['fields_views'][view]['toolbar']['print'].remove(pri)
                        if 'print' in res['fields_views'][view]['toolbar'].keys():
                            action = res['fields_views'][view]['toolbar']['action'][:]
                            for act in action:
                                if act['id'] in actions_and_prints:
                                    res['fields_views'][view]['toolbar']['action'].remove(act)
        return res

    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super()._get_view(view_id, view_type, **options)
        # access_management_obj = self.env['access.management']
        # cids = request.httprequest.cookies.get('cids') and request.httprequest.cookies.get('cids').split(',')[0] or request.env.company.id
        # readonly_access_id = access_management_obj.sudo().search(
        #     [('company_ids', 'in', self.env.company.id), ('active', '=', True), ('user_ids', 'in', self.env.user.id),
        #      ('readonly', '=', True)])

        readonly_access_id = search_data(self, 'access.management', condition=('readonly', '=', True), operator='AND')
        # access_recs = self.env['access.domain.ah'].sudo().search(
        #     [('access_management_id.user_ids', 'in', self.env.user.id), ('access_management_id.active', '=', True),
        #      ('model_id.model', '=', self._name)])
        
        # access_recs -= access_recs.filtered(lambda x: x.access_management_id.is_apply_on_without_company == False and self.env.company.id not in x.access_management_id.company_ids.ids)

        access_recs = search_data(self, 'access.domain.ah', search_model=self._name)

        # access_model_recs = self.env['remove.action'].sudo().search(
        #     [('access_management_id.user_ids', 'in', self.env.user.id),
        #      ('access_management_id.active', '=', True),
        #      ('model_id.model', '=', self._name)])
        
        # access_model_recs -= access_model_recs.filtered(lambda x: x.access_management_id.is_apply_on_without_company == False and self.env.company.id not in x.access_management_id.company_ids.ids)
        access_model_recs = search_data(self, 'remove.action', search_model=self._name)

        if view_type == 'form':
            # access_management_id = access_management_obj.sudo().search([
            #                                                      ('active', '=', True),
            #                                                      ('user_ids', 'in', self.env.user.id),
            #                                                      ('hide_chatter', '=', True)],
            #                                                     limit=1)
            access_management_id = search_data(self, 'access.management', condition=('hide_chatter', '=', True),operator='AND', limit=1)

            # if access_management_id and access_management_id.is_apply_on_without_company:
            #     for chatter_path in arch.xpath("//chatter"):
            #         chatter_path.getparent().remove(chatter_path)

            # elif self.env.company in access_management_id.company_ids:
            #     for chatter_path in arch.xpath("//chatter"):
            #         chatter_path.getparent().remove(chatter_path)
            if access_management_id:
                for chatter_path in arch.xpath("//chatter"):
                    chatter_path.getparent().remove(chatter_path)
            else:
                # hide_chatter_id = self.env['hide.chatter'].sudo().search([('access_management_id.active', '=', True),
                #                                     ('access_management_id.user_ids', 'in', self.env.user.id),
                #                                     ('model_id.model', '=', self._name),
                #                                     ('hide_chatter', '=', True)],
                #                                    limit=1)
                hide_chatter_id = search_data(self, 'hide.chatter', search_model=self._name, condition=('hide_chatter', '=', True), operator='AND', limit=1)

                # if hide_chatter_id and hide_chatter_id.access_management_id.is_apply_on_without_company:
                #     for chatter_path in arch.xpath("//chatter"):
                #         chatter_path.getparent().remove(chatter_path)

                # elif self.env.company in hide_chatter_id.access_management_id.company_ids:
                #     for chatter_path in arch.xpath("//chatter"):
                #         chatter_path.getparent().remove(chatter_path)
                if hide_chatter_id:
                    for chatter_path in arch.xpath("//chatter"):
                        chatter_path.getparent().remove(chatter_path)

        if view_type in ['kanban', 'list']:
            restrict_import = search_data(self, 'access.management', condition=('hide_import', '=', True), operator='AND', limit=1)
            # restrict_import = access_management_obj.sudo().search([
            #                                                 ('active', '=', True),
            #                                                 ('user_ids', 'in', self.env.user.id),
            #                                                 ('hide_import', '=', True)], limit=1)
            
            # restrict_import = restrict_import.filtered(lambda x: x.is_apply_on_without_company or self.env.company.id in x.company_ids.ids)
            if restrict_import or (access_model_recs and access_model_recs.filtered(lambda x: x.restrict_import)):
                doc = arch
                doc.attrib.update({'import': 'false'})
                arch = doc

            # restrict_export = access_management_obj.sudo().search([
            #                                                 ('active', '=', True),
            #                                                 ('user_ids', 'in', self.env.user.id),
            #                                                 ('hide_export', '=', True)], limit=1)
            # restrict_export = restrict_export.filtered(lambda x: x.is_apply_on_without_company or
            #                                             self.env.company.id in x.company_ids.ids)
            restrict_export = search_data(self, 'access.management', condition=('hide_export', '=', True), operator='AND', limit=1)

            if access_model_recs and (access_model_recs.filtered(lambda x: x.restrict_export) or restrict_export):
                doc = arch
                doc.attrib.update({'export_xlsx': 'false'})
                arch = doc

        if readonly_access_id:
            if view_type == 'form':
                arch.attrib.update({'create': 'false', 'delete': 'false', 'edit': 'false'})

            if view_type == 'list':
                arch.attrib.update({'create': 'false', 'delete': 'false', 'edit': 'false'})

            if view_type == 'kanban':
                arch.attrib.update({'create': 'false', 'delete': 'false', 'edit': 'false'})

        else:

            if access_model_recs:
                delete = 'true'
                edit = 'true'
                create = 'true'
                for access_model in access_model_recs:
                    if access_model.restrict_create:
                        create = 'false'
                    if access_model.restrict_edit:
                        edit = 'false'
                    if access_model.restrict_delete:
                        delete = 'false'

                if view_type == 'form':
                    arch.attrib.update({'create': create, 'delete': delete, 'edit': edit})

                if view_type == 'list':
                    arch.attrib.update({'create': create, 'delete': delete, 'edit': edit})

                if view_type == 'kanban':
                    arch.attrib.update({'create': create, 'delete': delete, 'edit': edit})

            if access_recs:
                delete = 'false'
                edit = 'false'
                create = 'false'
                for access_rec in access_recs:
                    if access_rec.create_right:
                        create = 'true'
                    if access_rec.write_right:
                        edit = 'true'
                    if access_rec.delete_right:
                        delete = 'true'

                if view_type == 'form':
                    arch.attrib.update({'create': create, 'delete': delete, 'edit': edit})

                if view_type == 'list':
                    arch.attrib.update({'create': create, 'delete': delete, 'edit': edit})

                if view_type == 'kanban':
                    arch.attrib.update({'create': create, 'delete': delete, 'edit': edit})

        return arch, view

    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #     res = super().fields_view_get(view_id, view_type, toolbar, submenu)
    #     access_management_obj = self.env['access.management']
    #     cids = request.httprequest.cookies.get('cids') and request.httprequest.cookies.get('cids').split(',')[0] or request.env.company.id
    #     readonly_access_id = access_management_obj.search([('company_ids','in',int(cids)),('active','=',True),('user_ids','in',self.env.user.id),('readonly','=',True)])

    #     access_recs = self.env['access.domain.ah'].search([('access_management_id.company_ids','in',self.env.company.id),('access_management_id.user_ids','in',self.env.user.id),('access_management_id.active','=',True),('model_id.model','=',res['model'])])
    #     access_model_recs = self.env['remove.action'].search([('access_management_id.company_ids','in',self.env.company.id),('access_management_id.user_ids','in',self.env.user.id),('access_management_id.active','=',True),('model_id.model','=',res['model'])])

    #     if view_type == 'form':
    #         # access_fields_recs = self.env['hide.field'].search([('access_management_id.company_ids','in',self.env.company.id),('access_management_id.user_ids','in',self.env.user.id),('access_management_id.active','=',True),('model_id.model','=',res['model']),('external_link','=',True)])
    #         # if access_fields_recs:
    #         #     doc = etree.XML(res['arch'])
    #         #     for field in access_fields_recs.mapped('field_id'):
    #         #         if field.ttype in ['many2many','many2one']:
    #         #             for field_ele in doc.xpath("//field[@name='" + field.name + "']"):
    #         #                 options = 'options' in field_ele.attrib.keys() and field_ele.attrib['options'] or "{}"
    #         #                 options = ast.literal_eval(options)
    #         #                 options.update({'no_create': True,'no_create_edit':True,'no_open':True})
    #         #                 field_ele.attrib.update({'options':str(options)})
    #         #     res['arch'] = etree.tostring(doc, encoding='unicode')        
    #         if access_management_obj.search([('company_ids','in',self.env.company.id),('active','=',True),('user_ids','in',self.env.user.id),('hide_chatter','=',True)],limit=1).id  or self.env['remove.action'].search([('access_management_id.company_ids','in',self.env.company.id),('access_management_id.active','=',True),('access_management_id.user_ids','in',self.env.user.id),('model_id.model','=',res['model']),('restrict_chatter','=',True)],limit=1):
    #             doc = etree.XML(res['arch'])
    #             for div in doc.xpath("//div[@class='oe_chatter']"):
    #                     div.getparent().remove(div)
    #             res['arch'] = etree.tostring(doc, encoding='unicode')

    #     if readonly_access_id:
    #         if view_type == 'form':
    #             doc = etree.XML(res['arch'])
    #             doc.attrib.update({'create':'false', 'delete':'false','edit':'false'})

    #             res['arch'] = etree.tostring(doc, encoding='unicode')
    #         if view_type == 'tree':
    #             doc = etree.XML(res['arch'])
    #             doc.attrib.update({'create':'false', 'delete':'false','edit':'false'})

    #             res['arch'] = etree.tostring(doc, encoding='unicode')

    #         if view_type == 'kanban':
    #             doc = etree.XML(res['arch'])
    #             doc.attrib.update({'create':'false', 'delete':'false','edit':'false'})

    #             res['arch'] = etree.tostring(doc, encoding='unicode').replace('&amp;quot;','&quot;')

    #     else:

    #         if access_model_recs:
    #             delete = 'true'
    #             edit = 'true'
    #             create = 'true'
    #             for access_model in access_model_recs:
    #                 if access_model.restrict_create:
    #                     create = 'false'
    #                 if access_model.restrict_edit:
    #                     edit = 'false'
    #                 if access_model.restrict_delete:
    #                     delete = 'false'

    #             if view_type == 'form':
    #                 doc = etree.XML(res['arch'])
    #                 doc.attrib.update({'create':create, 'delete':delete,'edit':edit})

    #                 res['arch'] = etree.tostring(doc, encoding='unicode')
    #             if view_type == 'tree':
    #                 doc = etree.XML(res['arch'])
    #                 doc.attrib.update({'create':create, 'delete':delete,'edit':edit})

    #                 res['arch'] = etree.tostring(doc, encoding='unicode')

    #             if view_type == 'kanban':
    #                 doc = etree.XML(res['arch'])
    #                 doc.attrib.update({'create':create, 'delete':delete,'edit':edit})

    #                 res['arch'] = etree.tostring(doc, encoding='unicode')

    #         if access_recs:
    #             delete = 'false'
    #             edit = 'false'
    #             create = 'false'
    #             for access_rec in access_recs:
    #                 if access_rec.create_right:
    #                     create = 'true'
    #                 if access_rec.write_right:
    #                     edit = 'true'
    #                 if access_rec.delete_right:
    #                     delete = 'true'

    #             if view_type == 'form':
    #                 doc = etree.XML(res['arch'])
    #                 doc.attrib.update({'create':create, 'delete':delete,'edit':edit})

    #                 res['arch'] = etree.tostring(doc, encoding='unicode')
    #             if view_type == 'tree':
    #                 doc = etree.XML(res['arch'])
    #                 doc.attrib.update({'create':create, 'delete':delete,'edit':edit})

    #                 res['arch'] = etree.tostring(doc, encoding='unicode')

    #             if view_type == 'kanban':
    #                 doc = etree.XML(res['arch'])
    #                 doc.attrib.update({'create':create, 'delete':delete,'edit':edit})

    #                 res['arch'] = etree.tostring(doc, encoding='unicode').replace('&amp;quot;','&quot;')
    #     return res

    def _get_access_management_domain_record(self, model=False):
        records = None
        try:
            if model:
                self._cr.execute(SQL("SELECT id FROM ir_model WHERE model='%s'" % model))
                model_numeric_id = self._cr.fetchone()[0]
                if model_numeric_id and isinstance(model_numeric_id, int) and self.env.user:
                    self._cr.execute(SQL("""
                                    SELECT dm.id
                                    FROM access_domain_ah as dm
                                    WHERE dm.model_id=%s AND dm.access_management_id 
                                    IN (SELECT am.id 
                                        FROM access_management as am 
                                        WHERE am.active='t' AND am.id 
                                        IN (SELECT amusr.access_management_id
                                            FROM access_management_users_rel_ah as amusr
                                            WHERE amusr.user_id=%s))
                                    """% (model_numeric_id, self.env.user.id)))
                    records = self.env['access.domain.ah'].sudo().browse(row[0] for row in self._cr.fetchall())
        except:
            pass
        return records

    def _check_access_management_right(self, mode=False, records=False):
        access_flag = False
        access_rule = None
        length = len(records.sudo()) if records.sudo() else 0
        partner_ids = self.env['res.users'].sudo().search([]).mapped("partner_id.id")
        partner_domain = ['|', ('id', 'in', partner_ids)]
        for record in records.sudo():
            if mode == 'create' and record.create_right:
                access_flag = True
                break
            elif mode in ['write', 'unlink']:
                access = False
                if mode == 'unlink':
                    access = record.delete_right
                elif mode == 'write':
                    access = record.write_right

                domain_list = []
                # eval_context = rec._eval_context()
                if self.sudo()._name == "res.partner":
                    domain_list += partner_domain
                dom = safe_eval(record.domain) if record.domain else []
                if dom:
                    dom = expression.normalize_domain(dom)
                    model_name = self._name
                    if isinstance(dom, list):
                        for dom_tuple in dom:
                            if isinstance(dom_tuple, tuple):
                                compute_domain(dom_tuple, model_name)
                                operator_value = dom_tuple[1]
                                # left_value = dom_tuple[0]
                                # operator_value = dom_tuple[1]
                                # right_value = dom_tuple[2]
                                # left_value_split_list = left_value.split('.')
                                # model_string = model_name
                                # left_user = False
                                # left_company = False
                                # for field in left_value_split_list:
                                #     left_user = False
                                #     left_company = False
                                #     model_obj = self.env[model_string]
                                #     field_type = model_obj.fields_get()[field]['type']
                                #     if field_type in ['many2one', 'many2many', 'one2many']:
                                #         field_relation = model_obj.fields_get()[field]['relation']
                                #         model_string = field_relation
                                #         if model_string == 'res.users':
                                #             left_user = True
                                #         if model_string == 'res.company':
                                #             left_company = True

                                # if left_user:
                                #     if operator_value in ['in', 'not in']:
                                #         if isinstance(right_value, list) and 0 in right_value:
                                #             zero_index = right_value.index(0)
                                #             right_value[zero_index] = self.env.user.id

                                # if left_company:
                                #     if operator_value in ['in', 'not in']:
                                #         if isinstance(right_value, list) and 0 in right_value:
                                #             zero_index = right_value.index(0)
                                #             right_value[zero_index] = self.env.company.id
                                already_add = False
                                if operator_value == 'date_filter':
                                    domain_list += prepare_domain_v2(dom_tuple)
                                else:
                                    domain_list.append(dom_tuple)
                            else:
                                domain_list.append(dom_tuple)
                    # domain_list.append(dom)
                search_domain = domain_list
                if 'active' in self._fields:
                    search_domain = ['|', ('active', '=', False), ('active', '=', True)] + search_domain
                record_ids = self.search(search_domain)

                if self in record_ids and access:
                    access_flag = access
                    break
            access_rule = record.access_management_id.name
        return {'access_flag': access_flag, 'access_rule': access_rule}

    def _display_access_management_error(self, mode=None, rule=None):
        if mode and rule:
            msg_heads = {
                'unlink': _(
                    "Due to access management rule,\nYou are not allowed to delete record '%(record)s' from (%(document_model)s) model.",
                    record=self.display_name, document_model=self._name),
                'write': _(
                    "Due to access management rule,\nYou are not allowed to edit record '%(record)s' from (%(document_model)s) model.",
                    record=self.display_name, document_model=self._name),
                'create': _(
                    "Due to access management rule,\nYou are not allowed to create records from (%(document_model)s) model.",
                    document_model=self.display_name),
            }
            operation_error = msg_heads[mode]
            resolution_info = _("Check Applied Rule on Access Management:\n %(access_name)s", access_name=rule)

            msg = """{operation_error}            

{resolution_info}""".format(operation_error=operation_error, resolution_info=resolution_info)
            raise AccessError(msg)

    def unlink(self):
        value = self.env['ir.config_parameter'].sudo().search([('key', '=', 'uninstall_simplify_access_management')],
                                                              limit=1).value
        if not value:
            for rec in self:
                if rec._name:
                    access_domain_ah_ids = rec._get_access_management_domain_record(model=rec._name)
                    if access_domain_ah_ids:
                        access_domain_ah_ids = access_domain_ah_ids.filtered(
                            lambda line: self.env.company in line.access_management_id.company_ids)
                    if access_domain_ah_ids:
                        flag = rec._check_access_management_right(mode='unlink', records=access_domain_ah_ids)
                        unlink_flag = flag['access_flag']
                        access_rule = flag['access_rule']
                        if not unlink_flag:
                            rec._display_access_management_error(mode='unlink', rule=access_rule)

        return super().unlink()

    def write(self, vals):
        value = self.env['ir.config_parameter'].sudo().search([('key', '=', 'uninstall_simplify_access_management')],
                                                              limit=1).value
        if not value:
            for rec in self:
                if rec._name:
                    access_domain_ah_ids = rec._get_access_management_domain_record(model=rec._name)
                    if access_domain_ah_ids:
                        access_domain_ah_ids = access_domain_ah_ids.filtered(
                            lambda line: self.env.company in line.access_management_id.company_ids)
                    if access_domain_ah_ids:
                        flag = rec._check_access_management_right(mode='write', records=access_domain_ah_ids)
                        write_flag = flag['access_flag']
                        access_rule = flag['access_rule']
                        if not write_flag:
                            rec._display_access_management_error(mode='write', rule=access_rule)
        return super().write(vals)
    
    # @api.model
    # def _name_search(self, name, domain=None, operator='ilike', limit=None, order=None):
    #     if not self.env.context.get('is_access_rights'):
    #         return super(BaseModel,self)._name_search(name, domain, operator, limit, order)
    #     domain = expression.AND([domain,[('name', 'ilike', name)]])
    #     return self._search(domain, limit=limit, order=order)

    @api.model_create_multi
    @api.returns('self', lambda value: value.id)
    def create(self, vals_list):
        value = self.env['ir.config_parameter'].sudo().search([('key','=','uninstall_simplify_access_management')],limit=1).value
        if not value:
            if self._name:
                access_domain_ah_ids = self._get_access_management_domain_record(model=self._name)
                if access_domain_ah_ids:
                    access_domain_ah_ids = access_domain_ah_ids.filtered(lambda line: self.env.company in line.access_management_id.company_ids)
                if access_domain_ah_ids:
                        flag = self._check_access_management_right(mode='create',records=access_domain_ah_ids)
                        create_flag = flag['access_flag']
                        access_rule = flag['access_rule']
                        if not create_flag:
                            self._display_access_management_error(mode='create',rule=access_rule)

        return super().create(vals_list)
