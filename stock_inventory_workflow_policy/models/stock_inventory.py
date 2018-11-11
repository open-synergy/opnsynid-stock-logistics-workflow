# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api, fields, SUPERUSER_ID


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    @api.multi
    @api.depends(
        "location_id",
    )
    def _compute_policy(self):
        for inventory in self:
            if self.env.user.id == SUPERUSER_ID:
                inventory.validate_ok = inventory.restart_ok = \
                    inventory.restart_ok = \
                    inventory.start_ok = inventory.cancel_ok = True
                continue

            if inventory.location_id:
                location = inventory.location_id
                for policy in location.\
                        _get_inventory_adjustment_button_policy_map():
                    setattr(
                        inventory,
                        policy[0],
                        location.
                        _get_inventory_adjustment_button_policy(
                            policy[1]),
                    )

    start_ok = fields.Boolean(
        string="Can Start",
        compute="_compute_policy",
        store=False,
        readonly=True,
    )
    validate_ok = fields.Boolean(
        string="Can Validate",
        compute="_compute_policy",
        store=False,
        readonly=True,
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
        store=False,
        readonly=True,
    )
    restart_ok = fields.Boolean(
        string="Can Restart",
        compute="_compute_policy",
        store=False,
        readonly=True,
    )
