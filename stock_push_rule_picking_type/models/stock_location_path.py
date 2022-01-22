# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class StockLocationPath(models.Model):
    _inherit = "stock.location.path"

    picking_type_ids = fields.Many2many(
        string="Picking Type",
        comodel_name="stock.picking.type",
        relation="rel_push_rule_2_type",
        col1="push_id",
        col2="picking_type_id",
    )
