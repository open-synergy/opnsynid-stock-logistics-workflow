# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.multi
    def action_done(self):
        _super = super(StockPicking, self)
        result = _super.action_done()
        dates = self.mapped("move_lines.date")
        self.write({"date_done": max(dates)})
        return result
