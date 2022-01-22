# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    confirm_group_ids = fields.Many2many(
        string="Allowed to Confirm",
        comodel_name="res.groups",
        rel="rel_picking_confirm",
        col1="type_id",
        col2="group_id",
    )
    force_group_ids = fields.Many2many(
        string="Allowed to Force Availability",
        comodel_name="res.groups",
        rel="rel_picking_force",
        col1="type_id",
        col2="group_id",
    )
    transfer_group_ids = fields.Many2many(
        string="Allowed to Transfer",
        comodel_name="res.groups",
        rel="rel_picking_transfer",
        col1="type_id",
        col2="group_id",
    )
    return_group_ids = fields.Many2many(
        string="Allowed to Reverse",
        comodel_name="res.groups",
        rel="rel_picking_return",
        col1="type_id",
        col2="group_id",
    )
    cancel_group_ids = fields.Many2many(
        string="Allowed to Cancel",
        comodel_name="res.groups",
        rel="rel_picking_cancel",
        col1="type_id",
        col2="group_id",
    )
    unreserve_group_ids = fields.Many2many(
        string="Allowed to Unreserve",
        comodel_name="res.groups",
        rel="rel_picking_unreserve",
        col1="type_id",
        col2="group_id",
    )
