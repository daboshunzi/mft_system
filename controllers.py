# -*- coding: utf-8 -*-

from openerp import http

class MFT_System(http.Controller):
    @http.route('/work_order/index', auth='public')
    def index(self):
        return 'HELLO WORLD!'

