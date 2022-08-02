# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def action_done(self):
        _super = super(StockPicking, self)
        result = _super.action_done()
        dates = self.mapped("move_lines.date")
        self.write({"date_done": max(dates)})
        return result
