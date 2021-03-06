# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.multi
    @api.depends(
        "picking_type_id",
    )
    def _compute_policy(self):
        _super = super(StockPicking, self)
        _super._compute_policy()

    invoice_ok = fields.Boolean(
        string="Can Invoice",
        compute="_compute_policy",
        store=False,
    )
