# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class StockPickingCancelReason(models.TransientModel):
    _name = "stock.picking.cancel"

    reason_id = fields.Many2one(
        comodel_name="stock.picking.cancel.reason", string="Reason", required=True
    )

    @api.multi
    def button_confirm(self):
        self.ensure_one()
        obj_stock_picking = self.env["stock.picking"]
        act_close = {"type": "ir.actions.act_window_close"}
        picking_ids = self._context.get("active_ids")
        if picking_ids is None:
            return act_close
        assert len(picking_ids) == 1, "Only 1 picking ID expected"
        picking = obj_stock_picking.browse(picking_ids)
        picking.cancel_reason_id = self.reason_id.id
        picking.action_cancel()
        return act_close
