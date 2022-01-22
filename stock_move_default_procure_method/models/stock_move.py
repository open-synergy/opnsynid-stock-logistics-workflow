# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.onchange("picking_type_id")
    def onchange_procure_method(self):
        picking_type = self.picking_type_id or False
        if picking_type:
            self.procure_method = (
                picking_type.default_move_procure_method or "make_to_stock"
            )
