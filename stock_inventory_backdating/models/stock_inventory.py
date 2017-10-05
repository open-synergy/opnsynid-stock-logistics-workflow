# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api, fields


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    backdate = fields.Datetime(
        string="Backdate",
    )

    @api.model
    def post_inventory(self, inv):
        ctx = {}
        if inv.backdate:
            ctx = {"move_date": inv.backdate}
        _super = super(StockInventory, self.with_context(ctx))
        _super.post_inventory(inv)

        if inv.backdate:
            for move in inv.move_ids:
                move.date = inv.backdate
                if move.quant_ids:
                    move.quant_ids.sudo().write({"in_date": inv.backdate})
