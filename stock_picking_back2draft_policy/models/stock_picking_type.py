# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    back2draft_group_ids = fields.Many2many(
        string="Allowed to Back To Draft",
        comodel_name="res.groups",
        rel="rel_picking_back2draft",
        col1="type_id",
        col2="group_id",
    )
