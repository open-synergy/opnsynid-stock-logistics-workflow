# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class StockPickingWave(models.Model):
    _inherit = "stock.picking.wave"

    type_id = fields.Many2one(
        string="Picking Wave Type",
        comodel_name="stock.picking_wave_type",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.model
    def create(self, vals):
        obj_ir_sequence = self.env["ir.sequence"]
        obj_stock_picking_wave_type = self.env["stock.picking_wave_type"]
        if vals.get("name", "/") == "/":
            type_id = vals.get("type_id", False)
            if type_id:
                picking_wave_type = obj_stock_picking_wave_type.browse(type_id)
                if picking_wave_type.sequence_id:
                    vals["name"] = obj_ir_sequence.next_by_id(
                        picking_wave_type.sequence_id.id
                    )
                else:
                    vals["name"] = obj_ir_sequence.get("picking.wave")
            else:
                vals["name"] = obj_ir_sequence.get("picking.wave")
        return super(StockPickingWave, self).create(vals)
