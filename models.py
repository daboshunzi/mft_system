# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import time
import openerp
from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request
from openerp.addons.web.controllers.main import content_disposition
import mimetypes
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import models

class ProductTestGroup(models.Model):
    _name = 'mft.product_test_group'

    _columns = {
        'name': fields.char(required=True,string='Product Test Group',readonly=True,states={'draft':[('readonly',False)]}),
        'description': fields.text(string='Description',readonly=True,states={'draft':[('readonly',False)]}),
        'procedure_line': fields.one2many('mft.procedure_group', 'test_group_id', string='Procedure',readonly=True,states={'draft':[('readonly',False)]}),
        'state': fields.selection([
            ('draft', 'Developping'),
            ('toconfirm', 'Pre-production'),
            ('confirmed', 'Production'),
            ('stopped', 'EOL'),
            ], 'State', readonly=True, copy=False),
    }

    _defaults = {
        'state': 'draft',
    }

    def action_toconfirm(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'toconfirm'})
        return True

    def action_confirmed(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'confirmed'})
        return True

    def action_stopped(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'stopped'})
        return True

    def action_recover(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'draft'})
        return True

    def unlink(self, cr, uid, ids, context=None):
        product_names = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        for p in product_names:
            if p['state'] in ['draft']:
                unlink_ids.append(p['id'])
            else:
                raise osv.except_osv(_('Invalid Action!'), 'Only draft can be deleted!')

        return osv.osv.unlink(self, cr, uid, unlink_ids, context=context)

class ProductName(models.Model):
    _name = 'mft.product_name'

    _columns = {
        'name': fields.char(required=True,string='Products',readonly=True, select=True,states={'draft':[('readonly',False)]}),
        'partnumber': fields.char(required=True,string='Part Number',readonly=True, select=True,states={'draft':[('readonly',False)]}),
        'test_group_id' : fields.many2one('mft.product_test_group',string="Product Test Group", required=False,readonly=True, select=True,states={'draft':[('readonly',False)]}),
        'description': fields.text(string='Description',readonly=True,states={'draft':[('readonly',False)]}),
        #'wo_ids': fields.one2many('mft.work_order','product_id',string='成品工单'),
        'product_env': fields.one2many('mft.product_env', 'product_id', string='Self-Defined ENV',readonly=True, select=True,states={'draft':[('readonly',False)]}),
        'procedure_line': fields.one2many('mft.procedure', 'product_id', string='Procedure',readonly=True, select=True,states={'draft':[('readonly',False)]}),
        'pcba_line': fields.one2many('mft.pd_pcba_line', 'product_id', string='PCBA',readonly=True, select=True,states={'draft':[('readonly',False)]}),
        'state': fields.selection([
            ('draft', 'Developping'),
            ('toconfirm', 'Pre-production'),
            ('confirmed', 'Production'),
            ('stopped', 'EOL'),
            ], 'State', readonly=True, copy=False, select=True),
        #'pcba_id': fields.many2many('mft.pcba_name','mft_product_pcb_rel','product_id','pcba_id', 'test'),
    }

    _defaults = {
        'state': 'draft',
    }

    def action_toconfirm(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'toconfirm'})
        return True

    def action_confirmed(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'confirmed'})
        return True

    def action_stopped(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'stopped'})
        return True

    def action_recover(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'draft'})
        return True

    def unlink(self, cr, uid, ids, context=None):
        product_names = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        for p in product_names:
            if p['state'] in ['draft']:
                unlink_ids.append(p['id'])
            else:
                raise osv.except_osv(_('Invalid Action!'), 'Only draft can be deleted!')

        return osv.osv.unlink(self, cr, uid, unlink_ids, context=context)

class OEMName(models.Model):
    _name = 'mft.oem_name'

    _columns = {
        'name': fields.char(string='OEM Name',readonly=True, select=True,states={'draft':[('readonly',False)]}),
        'language': fields.char(string='Language',readonly=True, select=True,states={'draft':[('readonly',False)]}),
        'website': fields.text(string='Website',readonly=True, select=True,states={'draft':[('readonly',False)]}),
        'oemname_env': fields.one2many('mft.oemname_env', 'oemname_id', string='Self-Defined ENV',readonly=True, select=True,states={'draft':[('readonly',False)]}),
        'description': fields.html(string='Description',readonly=True, select=True,states={'draft':[('readonly',False)]}),
        'state': fields.selection([
            ('draft', 'Draft'),
            ('toconfirm', 'Request Confirm'),
            ('confirmed', 'Confirmed'),
            ('cancel', 'Cancel'),
            ], 'State', readonly=True, copy=False, select=True),
        #'wo_ids': fields.one2many('mft.work_order','oem_id',string='成品工单')
    }

    _defaults = {
        'state': 'draft'
    }

    def action_toconfirm(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'toconfirm'})
        return True

    def action_confirmed(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'confirmed'})
        return True

    def action_recover(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'draft'})
        return True

    def unlink(self, cr, uid, ids, context=None):
        product_names = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        for p in product_names:
            if p['state'] in ['draft']:
                unlink_ids.append(p['id'])
            else:
                raise osv.except_osv(_('Invalid Action!'), 'Only draft can be deleted!')

        return osv.osv.unlink(self, cr, uid, unlink_ids, context=context)

class PrintTemplate(models.Model):
    _name = 'mft.print_template'

    _columns = {
        'name': fields.char(string='Template Name(EN)',size=8,readonly=True, select=True,states={'draft':[('readonly',False)]}),
        'nick': fields.char(string='Template Name(CN)',readonly=True,states={'draft':[('readonly',False)]}),
        'width': fields.char(string='Print Width',readonly=True,states={'draft':[('readonly',False)]}),
        'height': fields.char(string='Print Height',readonly=True,states={'draft':[('readonly',False)]}),
        'fn_fields': fields.char(string='Variables Name',readonly=True,states={'draft':[('readonly',False)]}),
        'template': fields.text(string='Template Content',readonly=True,states={'draft':[('readonly',False)]}),
        'description': fields.text(string='Description',readonly=True,states={'draft':[('readonly',False)]}),
        'state': fields.selection([
            ('draft', 'Draft'),
            ('toconfirm', 'Request Confirm'),
            ('confirmed', 'Confirmed'),
            ('cancel', 'Cancel'),
            ], 'State', readonly=True, copy=False),
    }

    _defaults = {
        'state': 'draft'
    }

    def action_toconfirm(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'toconfirm'})
        return True

    def action_confirmed(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'confirmed'})
        return True

    def action_recover(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'draft'})
        return True

    def unlink(self, cr, uid, ids, context=None):
        product_names = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        for p in product_names:
            if p['state'] in ['draft']:
                unlink_ids.append(p['id'])
            else:
                raise osv.except_osv(_('Invalid Action!'), 'Only draft can be deleted!')

        return osv.osv.unlink(self, cr, uid, unlink_ids, context=context)

class WorkOrders(osv.osv):
    _name = 'mft.work_order'

    _columns = {
        'name' : fields.char('Work Order',required=True, copy=False,readonly=True, select=True,states={'draft':[('readonly',False)]}),
        'ref_order': fields.char('Related Order', readonly=True, select=True,states={'draft':[('readonly',False)]}),
        'product_id' : fields.many2one('mft.product_name',string="Product Name", required=True,readonly=True, select=True,states={'draft':[('readonly',False)]}),
        'fw_version' : fields.char(string='Firmware Version', required=True,readonly=True,states={'draft':[('readonly',False)]}),
        'bt_version' : fields.char(string='uBoot Version', required=True,readonly=True,states={'draft':[('readonly',False)]}),
        'oem_id' : fields.many2one('mft.oem_name',string='OEM Name', required=True,readonly=True, select=True,states={'draft':[('readonly',False)]}),
        'count' : fields.integer(string='Count', required=True,readonly=True, select=True,states={'draft':[('readonly',False)]}),
        'products_ids' : fields.one2many('mft.products', 'wo_id', string='Products SN'),
        'state': fields.selection([
            ('draft', 'Draft'),
            ('toconfirm', 'Request Confirm'),
            ('confirmed', 'Confirmed'),
            ('done', 'Done'),
            ('cancel', 'Cancel'),
            ], 'State', readonly=True, copy=False, select=True),
    }

    _defaults = {
        'name' : lambda obj, cr, uid, context: '/',
        'state': 'draft'
    }

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if vals.get('name', '/') == '/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'mft.work_order') or '/'
        new_id = super(WorkOrders, self).create(cr, uid, vals,context)
        return new_id

    def action_toconfirm(self,cr,uid,ids,context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'toconfirm'})
        return True

    def action_confirmed(self,cr,uid,ids,context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'confirmed'})
        return True

    def action_cancel(self,cr,uid,ids,context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'cancel'})
        return True

    def action_done(self,cr,uid,ids,context=None):
        if context is None:
            context = {}
        pcbas = self.pool.get('mft.products').search(cr,uid,[('pass_flag','=',True),('wo_id','=',ids[0])])
        order = self.browse(cr, uid, ids, context=context)
        if len(pcbas) == order.count:
            self.write(cr, uid, ids, {'state': 'done'})
            return True

        info = "不能完成工单，数量不一致，已经通过测试的数量为：{0}，实际生产的数量为：{1}。".format(len(pcbas),order.count)
        raise osv.except_osv(_('Invalid Action!'), info)

    def action_recover(self,cr,uid,ids,context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'draft'})
        return True

    def unlink(self, cr, uid, ids, context=None):
        product_names = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        for p in product_names:
            if p['state'] in ['draft', 'cancel']:
                unlink_ids.append(p['id'])
            else:
                raise osv.except_osv(_('Invalid Action!'), 'Only draft or canceled order can be deleted!')

        return osv.osv.unlink(self, cr, uid, unlink_ids, context=context)

class SB_WorkOrders(osv.osv):
    _name = 'mft.sb_work_order'

    _columns = {
        'name' : fields.char('Work Order',required=True, copy=False, select=True),
        'ref_order': fields.char('Related Order'),
        'product_id' : fields.many2one('mft.product_name',string="Product Name", required=True, select=True),
        'fw_version' : fields.char(string='Firmware Version', required=True),
        'bt_version' : fields.char(string='uBoot Version', required=True),
        'oem_id' : fields.many2one('mft.oem_name',string='OEM Name', required=True, select=True),
        'count' : fields.integer(string='Count', required=True)
    }

    _defaults = {
        'name' : lambda obj, cr, uid, context: '/'
    }

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if vals.get('name', '/') == '/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'mft.sb_work_order') or '/'
        new_id = super(SB_WorkOrders, self).create(cr, uid, vals,context)
        return new_id

class Products(osv.Model):
    _name = 'mft.products'

    _columns = {
        'name': fields.char(string='Products SN', select=True),
        'wo_id': fields.many2one('mft.work_order', string='Work Order', select=True),
        'do_id': fields.many2one('mft.delivery_orders', string='Shipping Order', select=True),
        'product_id': fields.many2one('mft.product_name', string='Product Name', select=True),
        'oem_id': fields.many2one('mft.oem_name', string='OEM Name', select=True),
        'mac_addr': fields.char(string='MAC Address'),
        'pass_flag': fields.boolean(string='Pass Flag'),
        'test_ids': fields.one2many('mft.product_test', 'parts_id',string='Test Details'),
        'grouptest_ids': fields.one2many('mft.product_grouptest', 'parts_id',string='Group Test Details'),
        'pcba_line_ids': fields.one2many('mft.product_pcbas', 'product_sn', string="Composition"),
        'mac_addr2':fields.char(string='MAC Address 2'),
        'mac_addr3':fields.char(string='MAC Address 3'),
        'IMEI':fields.char(string='IMEI'),
        'module_version':fields.char(string='Module Version'),
        'ICCID':fields.char(string='ICCID'),
        'phone_number':fields.char(string='Phone Number'),
        'private_key':fields.char(string='Private Key'),
        'public_key':fields.char(string='Public Key'),
        'encryption_sn':fields.char(string='Encrypted Chip SN'),
        'device_cert':fields.char(string='Terminal Certificate')
        }

class ProcedureGroup(osv.Model):
    _name = 'mft.procedure_group'

    _columns = {
        'name': fields.char(string='Procedure Name', select=True),
        'number': fields.integer('Index', required=True),
        'test_group_id': fields.many2one('mft.product_test_group', select = True, string='Product Test Group Name'),
        'test_config': fields.text(string='Test Config')
    }

class Procedure(osv.Model):
    _name = 'mft.procedure'

    _columns = {
        'name': fields.char(string='Procedure Name', select=True),
        'number': fields.integer('Index', required=True),
        'product_id': fields.many2one('mft.product_name', select = True, string='Product Name'),
        'test_config': fields.text(string='Test Config')
    }

class Product_Env(osv.Model):
    _name = 'mft.product_env'

    _columns = {
        'product_id': fields.many2one('mft.product_name', string='Product Name', select=True),
        'name': fields.char(string='Name',required=True),
        'value': fields.char('Value', required=True)
    }

class OEMName_Env(osv.Model):
    _name = 'mft.oemname_env'

    _columns = {
        'oemname_id': fields.many2one('mft.oem_name', string='OEM Name', select=True),
        'name': fields.char(string='Name',required=True),
        'value': fields.char('Value', required=True)
    }

class ProductTest(models.Model):
    _name = 'mft.product_test'

    _columns = {
        'parts_id': fields.many2one('mft.products', string='Products SN', select=True),
        'test_result': fields.text(string='Test Result'),
        'pass_flag': fields.boolean(string='Pass Flag'),
        'procedure_id': fields.many2one('mft.procedure', select = True, string="Procedure"),
        'product_id': fields.many2one('mft.product_name', select = True, string="Product Name"),
        'test_user': fields.char("Worker")
    }

class ProductGroupTest(models.Model):
    _name = 'mft.product_grouptest'

    _columns = {
        'parts_id': fields.many2one('mft.products', string='Products SN', select=True),
        'test_result': fields.text(string='Test Result'),
        'pass_flag': fields.boolean(string='Pass Flag'),
        'procedure_id': fields.many2one('mft.procedure_group', select = True, string="Procedure"),
        'product_id': fields.many2one('mft.product_name', select = True, string="Product Name"),
        'test_user': fields.char("Worker")
    }

#记录产品由多少个模块组成的表
# name：一个描述，直接用模块的名称代替
# product_id：关联到mft.product_name中，多对一的关系
# pcba_id：关联到mft.pcba_name中，多对一的关系
class PdModLine(osv.osv):
    _name = 'mft.pd_pcba_line'

    _columns = {
        'name': fields.text(required=True, string="Description"),
        'product_id': fields.many2one('mft.product_name',  change_default=True, string="Product Name", select=True),
        'pcba_id': fields.many2one('mft.pcba_name', string="Module Name", select=True),
    }

    _defaults = {
        'name' : '',
    }

class ProductPCBAs(osv.Model):
    _name = 'mft.product_pcbas'

    _columns = {
        'pcba_line_id': fields.many2one('mft.pd_pcba_line', "Composition", select=True),
        'product_id': fields.many2one('mft.product_name', 'Product Name', select=True),
        'product_sn': fields.many2one('mft.products', 'Product SN', select=True),
        'pcba_name': fields.many2one('mft.pcba_name', 'PCBA Name', select=True),
        'pcba_sn': fields.many2one('mft.pcbas', 'PCBA SN', select=True)
    }

class PcbaTestGroup(models.Model):
    _name = 'mft.pcba_test_group'

    _columns = {
        'name': fields.char(required=True, string='PCBA Test Group',readonly=True, select=True,states={'draft':[('readonly',False)]}),
        'description': fields.text(string='Description',readonly=True,states={'draft':[('readonly',False)]}),
        #'po_ids': fields.one2many('mft.pcba_order','name_id',string='PCBA工单'),
        'procedure_line': fields.one2many('mft.pcba_procedure_group', 'pcba_test_group_id', string="Procedure",readonly=True, states={'draft':[('readonly',False)]}),
        'state': fields.selection([
            ('draft', 'Developping'),
            ('toconfirm','Pre-production'),
            ('confirmed', 'Production'),
            ('stopped', 'EOL'),
            ('cancel', 'Cancel'),
            ], 'State', readonly=True, copy=False),
    }

    _defaults = {
        'state': 'draft'
    }

    def action_toconfirm(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'toconfirm'})
        return True

    def action_confirmed(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'confirmed'})
        return True

    def action_stopped(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'stopped'})
        return True

    def action_recover(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'draft'})
        return True

    def unlink(self, cr, uid, ids, context=None):
        product_names = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        for p in product_names:
            if p['state'] in ['draft']:
                unlink_ids.append(p['id'])
            else:
                raise osv.except_osv(_('Invalid Action!'), 'Only draft can be deleted!')

        return osv.osv.unlink(self, cr, uid, unlink_ids, context=context)

class PcbaName(models.Model):
    _name = 'mft.pcba_name'

    _columns = {
        'name': fields.char(required=True, string='PCBA Name',readonly=True, select=True,states={'draft':[('readonly',False)]}),
        'partnumber': fields.char(string='Part Number',readonly=True, select=True,states={'draft':[('readonly',False)]}),
        'test_group_id': fields.many2one('mft.pcba_test_group', string='PCBA Test Group', required=False,readonly=True, select=True,states={'draft':[('readonly',False)]}),
        'description': fields.text(string='Description',readonly=True,states={'draft':[('readonly',False)]}),
        #'po_ids': fields.one2many('mft.pcba_order','name_id',string='PCBA工单'),
        'pcba_env': fields.one2many('mft.pcba_env', 'pcba_id', string='Self-Defined ENV',readonly=True,states={'draft':[('readonly',False)]}),
        'procedure_line': fields.one2many('mft.pcba_procedure', 'pcba_id', string="Procedure",readonly=True,states={'draft':[('readonly',False)]}),
        'state': fields.selection([
            ('draft', 'Developping'),
            ('toconfirm','Pre-production'),
            ('confirmed', 'Production'),
            ('stopped', 'EOL'),
            ('cancel', 'Cancel'),
            ], 'State', readonly=True, copy=False),
    }

    _defaults = {
        'state': 'draft'
    }

    def action_toconfirm(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'toconfirm'})
        return True

    def action_confirmed(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'confirmed'})
        return True

    def action_stopped(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'stopped'})
        return True

    def action_recover(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'draft'})
        return True

    def unlink(self, cr, uid, ids, context=None):
        product_names = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        for p in product_names:
            if p['state'] in ['draft']:
                unlink_ids.append(p['id'])
            else:
                raise osv.except_osv(_('Invalid Action!'), 'Only draft can be deleted!')

        return osv.osv.unlink(self, cr, uid, unlink_ids, context=context)

class PcbaOrders(osv.osv):
    _name = 'mft.pcba_order'

    _columns = {
        'name': fields.char(required=True,string='PCBA Order',copy=False,readonly=True, select=True,states={'draft':[('readonly',False)]}),
        'ref_order': fields.char("Related Order", readonly=True, select=True,states={'draft':[('readonly',False)]}),
        'fw_version': fields.char(string='Firmware Version', required=True, readonly=True,states={'draft':[('readonly',False)]}),
        'bt_version': fields.char(string='uBoot Version', required=True, readonly=True,states={'draft':[('readonly',False)]}),
        'description': fields.text(string='Description',readonly=True,states={'draft':[('readonly',False)]}),
        'count': fields.integer(string='Count', required=True, readonly=True,states={'draft':[('readonly',False)]}),
        'name_id': fields.many2one('mft.pcba_name', string='PCBA Name', required=True,readonly=True, select=True,states={'draft':[('readonly',False)]}),
        'pcba_ids': fields.one2many('mft.pcbas','order_id',string='PCBA SN'),
        'state': fields.selection([
            ('draft', 'Draft'),
            ('toconfirm','Request Confirm'),
            ('confirmed', 'Confirmed'),
            ('done','Done'),
            ('cancel', 'Cancel'),
            ], 'State', readonly=True, copy=False),
    }

    _defaults = {
        'name': lambda obj, cr, uid, context: '/',
        'state': 'draft'
    }

    def create( self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if vals.get('name', '/') == '/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'mft.pcba_order') or '/'
        new_id = super(PcbaOrders, self).create(cr, uid, vals,context)
        return new_id

    def action_toconfirm(self,cr,uid,ids,context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'toconfirm'})
        return True

    def action_confirmed(self,cr,uid,ids,context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'confirmed'})
        return True

    def action_cancel(self,cr,uid,ids,context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'cancel'})
        return True

    def action_done(self,cr,uid,ids,context=None):
        if context is None:
            context = {}
        pcbas = self.pool.get('mft.pcbas').search(cr,uid,[('pass_flag','=',True),('order_id','=',ids[0])])
        order = self.browse(cr, uid, ids, context=context)
        if len(pcbas) == order.count:
            self.write(cr, uid, ids, {'state': 'done'})
            return True

        info = "不能完成工单，数量不一致，已经通过测试的数量为：{0}，实际生产的数量为：{1}。".format(len(pcbas),order.count)
        raise osv.except_osv(_('Invalid Action!'), info)

    def action_recover(self,cr,uid,ids,context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'draft'})
        return True

    def unlink(self, cr, uid, ids, context=None):
        product_names = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        for p in product_names:
            if p['state'] in ['draft', 'cancel']:
                unlink_ids.append(p['id'])
            else:
                raise osv.except_osv(_('Invalid Action!'), '只有草稿和取消的工单可以删除！')

        return osv.osv.unlink(self, cr, uid, unlink_ids, context=context)

class SB_PcbaOrders(osv.osv):
    _name = 'mft.sb_pcba_order'

    _columns = {
        'name': fields.char(required=True,string='PCBA Order',copy=False, select=True),
        'ref_order': fields.char("Related Order"),
        'fw_version': fields.char(string='Firmware Version', required=True),
        'bt_version': fields.char(string='uBoot Version', required=True),
        'description': fields.text(string='Description'),
        'count': fields.integer(string='Count', required=True),
        'name_id': fields.many2one('mft.pcba_name', string='PCBA Name', required=True, select=True),
    }

    _defaults = {
        'name': lambda obj, cr, uid, context: '/'
    }

    def create( self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if vals.get('name', '/') == '/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'mft.sb_pcba_order') or '/'
        new_id = super(SB_PcbaOrders, self).create(cr, uid, vals,context)
        return new_id

class PCBAs(models.Model):
    _name = 'mft.pcbas'

    _columns = {
        'name': fields.char(required=True,string='PCBA SN', select=True),
        'pass_flag': fields.boolean(string='Pass Flag', select=True),
        'order_id': fields.many2one('mft.pcba_order',string='PCBA Order', select=True),
        'pcba_id': fields.many2one('mft.pcba_name', string="PCBA Name", select=True),
        'test_ids': fields.one2many('mft.pcba_test', 'parts_id', string='Test Details'),
        'grouptest_ids': fields.one2many('mft.pcba_grouptest', 'parts_id', string='Group Test Details')
    }

class PCBATest(models.Model):
    _name = 'mft.pcba_test'

    _columns = {
        'pcba_id': fields.many2one('mft.pcba_name', string="PCBA Name", select=True),
        'parts_id': fields.many2one('mft.pcbas', string='PCBA SN', select=True),
        'procedure_id': fields.many2one('mft.pcba_procedure', string='Procedure', select=True),
        'pass_flag': fields.boolean(string='Pass Flag', select=True),
        'test_result': fields.char(string='Test Result'),
        'test_user': fields.char('Worker')
    }

class PCBAGroupTest(models.Model):
    _name = 'mft.pcba_grouptest'

    _columns = {
        'pcba_id': fields.many2one('mft.pcba_name', string="PCBA Name", select=True),
        'parts_id': fields.many2one('mft.pcbas', string='PCBA SN', select=True),
        'procedure_id': fields.many2one('mft.pcba_procedure_group', string='Procedure', select=True),
        'pass_flag': fields.boolean(string='Pass Flag', select=True),
        'test_result': fields.char(string='Test Result'),
        'test_user': fields.char('Worker')
    }

class PCBAProcedure(osv.Model):
    _name = 'mft.pcba_procedure'

    _columns = {
        'name': fields.char(string='Procedure Name', select=True),
        'number': fields.integer('Index', required=True),
        'pcba_id': fields.many2one('mft.pcba_name', string='PCBA Name', select=True),
        'test_config': fields.text(string='Test Config')
    }

class PCBAProcedureGroup(osv.Model):
    _name = 'mft.pcba_procedure_group'

    _columns = {
        'name': fields.char(string='Procedure Name', select=True),
        'number': fields.integer('Index', required=True),
        'pcba_test_group_id': fields.many2one('mft.pcba_grouptest', string='PCBA Test Group', select=True),
        'test_config': fields.text(string='Test Config')
    }

class Pcba_Env(osv.Model):
    _name = 'mft.pcba_env'

    _columns = {
        'pcba_id': fields.many2one('mft.pcba_name', string='PCBA Name', select=True),
        'name': fields.char(string='Name',required=True),
        'value': fields.char('Value', required=True)
    }

class DeliveryOrders(osv.osv):
    _name = 'mft.delivery_orders'

    _columns = {
        'name' : fields.char('Shipping Order',required=True, copy=False,readonly=True, select=True,states={'draft':[('readonly',False)]}),
        'sale_order': fields.char('Sales Order', readonly=True, states={'draft':[('readonly',False)]}),
        'customer': fields.char('Customer Name', readonly=True, states={'draft':[('readonly',False)]}),
        'address': fields.char('Address', readonly=True, states={'draft':[('readonly',False)]}),
        'contact_number': fields.char('Contact Number', readonly=True, states={'draft':[('readonly',False)]}),
        'sales_name': fields.char('Sales', readonly=True, states={'draft':[('readonly',False)]}),
        'sales_phone': fields.char('Sales Phone', readonly=True, states={'draft':[('readonly',False)]}),
        'delivery_company' : fields.many2one('mft.delivery_company',string="Delivery Company", required=True,readonly=True, select=True,states={'draft':[('readonly',False)]}),
        'delivery_number': fields.char('Delivery Number', readonly=True,states={'draft':[('readonly',False)]}),
        'delivery_state': fields.text('Delivery State', readonly=True,states={'draft':[('readonly',False)]}),
        'delivery_list' : fields.one2many('mft.delivery_list', 'do_id', string='Delivery List'),
        'delivery_sn' : fields.one2many('mft.products', 'do_id', string='Product SN'),
        'notes': fields.text(string='Note',readonly=True,states={'draft':[('readonly',False)]}),
        'state': fields.selection([
            ('draft', 'Draft'),
            ('toconfirm', 'Request Confirm'),
            ('confirmed', 'Confirmed'),
            ('done', 'Done'),
            ('cancel', 'Cancel'),
            ], 'State', readonly=True, copy=False),
    }

    _defaults = {
        'name' : lambda obj, cr, uid, context: '/',
        'state': 'draft'
    }

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        if vals.get('name', '/') == '/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'mft.delivery_orders') or '/'
        new_id = super(DeliveryOrders, self).create(cr, uid, vals,context)
        return new_id

    def action_toconfirm(self,cr,uid,ids,context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'toconfirm'})
        return True

    def action_confirmed(self,cr,uid,ids,context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'confirmed'})
        return True

    def action_cancel(self,cr,uid,ids,context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'cancel'})
        return True

    def action_done(self,cr,uid,ids,context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'done'})
        return True
        '''
        pcbas = self.pool.get('mft.products').search(cr,uid,[('pass_flag','=',True),('wo_id','=',ids[0])])
        order = self.browse(cr, uid, ids, context=context)
        if len(pcbas) == order.count:
            self.write(cr, uid, ids, {'state': 'done'})
            return True

        info = "不能完成工单，数量不一致，已经通过测试的数量为：{0}，实际生产的数量为：{1}。".format(len(pcbas),order.count)
        raise osv.except_osv(_('Invalid Action!'), info)
        '''

    def action_recover(self,cr,uid,ids,context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'draft'})
        return True

    def unlink(self, cr, uid, ids, context=None):
        product_names = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        for p in product_names:
            if p['state'] in ['draft', 'cancel']:
                unlink_ids.append(p['id'])
            else:
                raise osv.except_osv(_('Invalid Action!'), '只有草稿和取消的发货单可以删除！')

        return osv.osv.unlink(self, cr, uid, unlink_ids, context=context)

class DeliveryCompany(models.Model):
    _name = 'mft.delivery_company'

    _columns = {
        'name': fields.char(string='Delivery Company',readonly=True,states={'draft':[('readonly',False)]}),
        'contact_name': fields.char(string='Contact Name',readonly=True,states={'draft':[('readonly',False)]}),
        'contact_phone': fields.char(string='Contact Phone',readonly=True,states={'draft':[('readonly',False)]}),
        'description': fields.html(string='Description',readonly=True,states={'draft':[('readonly',False)]}),
        'state': fields.selection([
            ('draft', 'Draft'),
            ('toconfirm', 'Request Confirm'),
            ('confirmed', 'Confirmed'),
            ('cancel', 'Cancel'),
            ], 'State', readonly=True, copy=False),
        #'wo_ids': fields.one2many('mft.work_order','oem_id',string='成品工单')
    }

    _defaults = {
        'state': 'draft'
    }

    def action_toconfirm(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'toconfirm'})
        return True

    def action_confirmed(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'confirmed'})
        return True

    def action_recover(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        self.write(cr, uid, ids, {'state': 'draft'})
        return True

    def unlink(self, cr, uid, ids, context=None):
        product_names = self.read(cr, uid, ids, ['state'], context=context)
        unlink_ids = []
        for p in product_names:
            if p['state'] in ['draft']:
                unlink_ids.append(p['id'])
            else:
                raise osv.except_osv(_('Invalid Action!'), '只有草稿才能删除！')

        return osv.osv.unlink(self, cr, uid, unlink_ids, context=context)

class DeliveryList(osv.Model):
    _name = 'mft.delivery_list'

    _columns = {
        'do_id': fields.many2one('mft.delivery_orders', "Shipping Order"),
        'part_number': fields.char(string='Part Number'),
        'product_name': fields.char(string='Product Name'),
        'unit': fields.char(string='Unit'),
        'count': fields.char(string='Count')
    }
