# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api
from openerp.tools.translate import _
from openerp.exceptions import Warning as UserError


class StockReturnPicking(models.TransientModel):
    _inherit = "stock.return.picking"

    @api.multi
    def action_return_picking(self):
        self.ensure_one()
        record_id = self.env.context.get("active_id", False) or False
        obj_picking = self.env["stock.picking"]
        pick = obj_picking.browse([record_id])[0]
        returned_lines = 0

        self._cancel_assignment(pick)

        new_picking = pick.copy(self._prepare_new_picking(pick))
        for line in self.product_return_moves:
            res = line._prepare_new_move(pick, new_picking)
            if not res:
                continue
            returned_lines += 1
            line.move_id.copy(res)

        if not returned_lines:
            strWarning = _("Please specify at least one non-zero quantity")
            raise UserError(strWarning)

        new_picking.action_confirm()
        new_picking.action_assign()

    @api.multi
    def _cancel_assignment(self, picking):
        self.ensure_one()
        obj_move = self.env["stock.move"]
        move_to_unreserve = []
        for move in picking.move_lines:
            to_check_moves = [
                move.move_dest_id] if move.move_dest_id.id else []
            while to_check_moves:
                current_move = to_check_moves.pop()
                if current_move.state not in ("done", "cancel") and \
                        current_move.reserved_quant_ids:
                    move_to_unreserve += current_move
                criteria = [
                    ("split_from", "=", current_move.id),
                ]
                split_moves = obj_move.search(criteria)
                if len(split_moves) > 0:
                    to_check_moves += split_moves

        if move_to_unreserve:
            move_to_unreserve.do_unreserve()
            move_to_unreserve.write({"move_orig_ids": False})

    @api.multi
    def _prepare_new_picking(self, picking):
        self.ensure_one()
        pick_type_id = picking.picking_type_id.return_picking_type_id and \
            picking.picking_type_id.return_picking_type_id.id or \
            picking.picking_type_id.id
        res = {
            "move_lines": [],
            "picking_type_id": pick_type_id,
            "state": "draft",
            "origin": picking.name,
        }
        return res


class StockReturnPickingLine(models.Model):
    _inherit = "stock.return.picking.line"

    @api.multi
    def _prepare_new_move(self, old_picking, new_picking):
        move = self.move_id
        new_qty = self.quantity
        if new_qty:
            if move.origin_returned_move_id.move_dest_id.id and \
                    move.origin_returned_move_id.state != "cancel":
                move_dest_id = move.origin_returned_move_id.move_dest_id.id
            else:
                move_dest_id = False
            new_uos_qty = new_qty * move.product_uos_qty / move.product_uom_qty
            res = {
                "product_id": self.product_id.id,
                "product_uom_qty": new_qty,
                "product_uos_qty": new_uos_qty,
                "picking_id": new_picking.id,
                "state": "draft",
                "location_id": move.location_dest_id.id,
                "location_dest_id": move.location_id.id,
                "picking_type_id": new_picking.picking_type_id.id,
                "warehouse_id": old_picking.picking_type_id.warehouse_id.id,
                "origin_returned_move_id": move.id,
                "procure_method": "make_to_stock",
                "restrict_lot_id": self.lot_id.id,
                "move_dest_id": move_dest_id,
            }
            return res
        else:
            return False
