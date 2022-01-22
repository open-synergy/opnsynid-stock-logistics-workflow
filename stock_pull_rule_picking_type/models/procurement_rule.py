# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ProcurementRule(models.Model):
    _inherit = "procurement.rule"

    picking_type_ids = fields.Many2many(
        string="Picking Type",
        comodel_name="stock.picking.type",
        relation="rel_pull_rule_2_type",
        col1="pullid",
        col2="picking_type_id",
    )
