# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class StockProductionLot(models.Model):
    _name = "stock.production.lot"
    _inherit = [
        "stock.production.lot",
        "base.sequence_document",
    ]

    @api.model
    def _default_name(self):
        return "/"

    name = fields.Char(
        string="Serial Number",
        required=True,
        help="Unique Serial Number",
        default=lambda self: self._default_name(),
    )

    @api.model
    def create(self, values):
        _super = super(StockProductionLot, self)
        result = _super.create(values)
        ctx = self.env.context.copy()
        date_sequence = self.env.context.get("date_sequence", fields.Date.today())
        ctx.update(
            {
                "ir_sequence_date": date_sequence,
            }
        )
        sequence = result.with_context(ctx)._create_sequence()
        result.write(
            {
                "name": sequence,
            }
        )
        return result
