# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, models
from openerp.exceptions import Warning as UserError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.constrains("picking_type_id", "wave_id")
    def _check_picking_type_id(self):
        for picking in self:
            picking_type_id = picking.picking_type_id

            if not picking.wave_id or not picking.picking_type_id:
                continue

            if not picking.wave_id.type_id:
                continue

            wave_type = picking.wave_id.type_id
            if picking.picking_type_id not in wave_type.allowed_picking_type_ids:
                strWarning = _("%s not allowed") % (picking_type_id.name)
                raise UserError(_("Warning"), strWarning)
