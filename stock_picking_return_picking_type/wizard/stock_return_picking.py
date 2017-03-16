# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields


class StockReturnPicking(models.TransientModel):
    _inherit = "stock.return.picking"

    picking_type_id = fields.Many2one(
        string="Picking Type",
        comodel_name="stock.picking.type",
    )

    @api.multi
    def _prepare_new_picking(self, picking):
        self.ensure_one()
        result = super(StockReturnPicking, self)._prepare_new_picking(picking)
        if self.picking_type_id:
            result["picking_type_id"] = \
                self.picking_type_id.id
        return result
