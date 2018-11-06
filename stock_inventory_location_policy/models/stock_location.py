# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class StockLocation(models.Model):
    _inherit = "stock.location"

    @api.depends(
        "allowed_group_inventory_ids",
        "allowed_user_inventory_ids")
    def _compute_all_user_inventory_ids(self):
        obj_res_users = self.env["res.users"]
        for location in self:
            users = location.allowed_user_inventory_ids
            group_ids = location.allowed_group_inventory_ids.ids
            criteria = [
                ("groups_id", "in", group_ids)
            ]
            users += obj_res_users.search(criteria)
            location.all_user_inventory_ids = users

    allowed_group_inventory_ids = fields.Many2many(
        string="Allowed Groups to Iventory Adjustments",
        comodel_name="res.groups",
        relation="relation_location_2_groups_inventory",
        column1="location_id",
        column2="group_inventory_id",
    )
    allowed_user_inventory_ids = fields.Many2many(
        string="Allowed Users to Iventory Adjustments",
        comodel_name="res.users",
        relation="relation_location_2_user_inventory",
        column1="location_id",
        column2="user_inventory_id",
    )
    all_user_inventory_ids = fields.Many2many(
        string="All Allowed Users for Iventory Adjustments",
        comodel_name="res.users",
        compute="_compute_all_user_inventory_ids",
        store=True,
        relation="relation_location_2_user_all_inventory",
        column1="location_id",
        column2="user_inventory_id",
    )
