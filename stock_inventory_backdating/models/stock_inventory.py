# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    backdate = fields.Datetime(
        string="Backdate",
    )

    @api.model
    def post_inventory(self):
        context = self._context.copy()
        if self.backdate:
            ctx = {
                "force_period_date": self.backdate,
            }
            context.update(ctx)
        return super(StockInventory, self.with_context(context)).post_inventory()
