# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class StockLocation(models.Model):
    _inherit = "stock.location"

    inventory_adjustment_force_grp_ids = fields.Many2many(
        string="Allowed To Force Validation Inventory Adjustment",
        comodel_name="res.groups",
        relation="rel_inventory_adjustment_allowed_force_groups",
        column1="location_id",
        column2="group_id",
    )

    @api.model
    def _get_inventory_adjustment_button_policy_map(self):
        _super = super(StockLocation, self)
        result = _super._get_inventory_adjustment_button_policy_map()
        result.append(("force_ok", "inventory_adjustment_force_grp_ids"))
        return result
