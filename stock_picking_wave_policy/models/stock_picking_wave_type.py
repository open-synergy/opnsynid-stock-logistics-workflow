# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class StockPickingWaveType(models.Model):
    _inherit = "stock.picking_wave_type"

    confirm_group_ids = fields.Many2many(
        string="Allowed to Confirm",
        comodel_name="res.groups",
        rel="rel_stock_picking_wave_confirm",
        col1="type_id",
        col2="group_id",
    )

    done_group_ids = fields.Many2many(
        string="Allowed to Done",
        comodel_name="res.groups",
        rel="rel_stock_picking_wave_done",
        col1="type_id",
        col2="group_id",
    )

    cancel_group_ids = fields.Many2many(
        string="Allowed to Cancel",
        comodel_name="res.groups",
        rel="rel_stock_picking_wave_done",
        col1="type_id",
        col2="group_id",
    )
