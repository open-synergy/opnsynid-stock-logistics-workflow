# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class StockPickingWaveType(models.Model):
    _name = "stock.picking_wave_type"
    _description = "Stock Picking Wave Type"

    name = fields.Char(
        string="Picking Wave Type",
        required=True,
    )
    sequence_id = fields.Many2one(string="Sequence", comodel_name="ir.sequence")
    warehouse_id = fields.Many2one(string="Warehouse", comodel_name="stock.warehouse")
    allowed_picking_type_ids = fields.Many2many(
        string="Allowed Picking Type",
        comodel_name="stock.picking.type",
        relation="picking_wave_type_rel",
        column1="picking_wave_type_id",
        column2="picking_type_id",
    )
