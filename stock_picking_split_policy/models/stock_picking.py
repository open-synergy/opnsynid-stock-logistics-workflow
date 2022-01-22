# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.multi
    @api.depends(
        "picking_type_id",
    )
    def _compute_policy(self):
        _super = super(StockPicking, self)
        _super._compute_policy()

    split_ok = fields.Boolean(
        string="Can Split",
        compute="_compute_policy",
        store=False,
    )
