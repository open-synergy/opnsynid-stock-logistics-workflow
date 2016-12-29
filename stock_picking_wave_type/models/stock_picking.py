# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, _
from openerp.exceptions import Warning as UserError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.constrains(
        'picking_type_id', 'wave_id.type_id.allowed_picking_type_ids')
    def _check_picking_type_id(self):
        type_id = self.wave_id.type_id
        allowed_picking_type_ids =\
            self.wave_id.type_id.allowed_picking_type_ids
        picking_type_id = self.picking_type_id

        if type_id:
            if picking_type_id not in allowed_picking_type_ids:
                strWarning = _("%s not allowed") % (picking_type_id.name)
                raise UserError(_('Warning'), strWarning)
