# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class StockLocation(models.Model):
    _inherit = "stock.location"

    inventory_adjustment_start_grp_ids = fields.Many2many(
        string="Allowed To Start Inventory Adjustment",
        comodel_name="res.groups",
        relation="rel_inventory_adjustment_allowed_confirm_groups",
        column1="location_id",
        column2="group_id",
    )
    inventory_adjustment_validate_grp_ids = fields.Many2many(
        string="Allowed To Validate Inventory Adjustment",
        comodel_name="res.groups",
        relation="rel_inventory_adjustment_allowed_validate_groups",
        column1="location_id",
        column2="group_id",
    )
    inventory_adjustment_restart_grp_ids = fields.Many2many(
        string="Allowed To Restart Inventory Adjustment",
        comodel_name="res.groups",
        relation="rel_inventory_adjustment_allowed_restart_groups",
        column1="location_id",
        column2="group_id",
    )
    inventory_adjustment_cancel_grp_ids = fields.Many2many(
        string="Allowed To Cancel` Inventory Adjustment",
        comodel_name="res.groups",
        relation="rel_inventory_adjustment_allowed_cancel_groups",
        column1="location_id",
        column2="group_id",
    )

    @api.model
    def _get_inventory_adjustment_button_policy_map(self):
        return [
            ("validate_ok", "inventory_adjustment_validate_grp_ids"),
            ("start_ok", "inventory_adjustment_start_grp_ids"),
            ("cancel_ok", "inventory_adjustment_cancel_grp_ids"),
            ("restart_ok", "inventory_adjustment_restart_grp_ids"),
        ]

    @api.multi
    def _get_inventory_adjustment_button_policy(self, policy_field):
        self.ensure_one()
        result = False
        button_group_ids = []
        user = self.env.user
        group_ids = user.groups_id.ids

        button_group_ids += getattr(self, policy_field).ids

        if not button_group_ids:
            result = True
        else:
            if set(button_group_ids) & set(group_ids):
                result = True
        return result
