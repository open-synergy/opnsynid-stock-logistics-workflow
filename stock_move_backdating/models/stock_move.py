# Copyright 2015-2016 Agile Business Group (<http://www.agilebg.com>)
# Copyright 2015 BREMSKERL-REIBBELAGWERKE EMMERLING GmbH & Co. KG
#    Author Marco Dieckhoff
# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = "stock.move"

    date_backdating = fields.Datetime(
        string="Actual Movement Date",
    )

    @api.constrains("date_backdating")
    def _check_date_backdating(self):
        now = fields.Datetime.now()
        for move in self:
            if move.date_backdating and move.date_backdating > now:
                raise UserError(
                    _("You can not process an actual " "movement date in the future.")
                )

    def _update_svl_backdate(self, move):
        if len(move.stock_valuation_layer_ids) > 0:
            query = """
                UPDATE public.stock_valuation_layer
                    SET create_date = %(create_date)s
                WHERE id IN %(svl_ids)s
            """
            params = {
                "create_date": move.date_backdating,
                "svl_ids": tuple(move.stock_valuation_layer_ids.ids),
            }
            self._cr.execute(query, params)

    def _action_done(self, cancel_backorder=False):
        _super = super(StockMove, self)
        result = _super._action_done(cancel_backorder=cancel_backorder)
        for move in self:
            if move.date_backdating:
                move.write(
                    {
                        "date": move.date_backdating,
                    }
                )
                self._update_svl_backdate(move)
        return result

    def _account_entry_move(self, qty, description, svl_id, cost):
        context = self._context.copy()
        if self.date_backdating:
            ctx = {
                "force_period_date": self.date_backdating,
            }
            context.update(ctx)
        return super(StockMove, self.with_context(context))._account_entry_move(
            qty, description, svl_id, cost
        )
