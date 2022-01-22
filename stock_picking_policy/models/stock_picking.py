# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class StockPicking(models.Model):
    _name = "stock.picking"
    _inherit = ["stock.picking", "base.workflow_policy_object"]

    @api.multi
    @api.depends(
        "picking_type_id",
    )
    def _compute_policy(self):
        _super = super(StockPicking, self)
        _super._compute_policy()

    confirm_ok = fields.Boolean(
        string="Can Confirm",
        compute="_compute_policy",
        store=False,
    )
    force_ok = fields.Boolean(
        string="Can Force Availability",
        compute="_compute_policy",
        store=False,
    )
    transfer_ok = fields.Boolean(
        string="Can Transfer",
        compute="_compute_policy",
        store=False,
    )
    return_ok = fields.Boolean(
        string="Can Return",
        compute="_compute_policy",
        store=False,
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
        store=False,
    )
    unreserve_ok = fields.Boolean(
        string="Can Unreserve",
        compute="_compute_policy",
        store=False,
    )
