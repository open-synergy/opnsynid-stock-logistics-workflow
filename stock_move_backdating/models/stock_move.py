# Copyright 2015-2016 Agile Business Group (<http://www.agilebg.com>)
# Copyright 2015 BREMSKERL-REIBBELAGWERKE EMMERLING GmbH & Co. KG
#    Author Marco Dieckhoff
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
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

    @api.multi
    def _action_done(self):
        _super = super(StockMove, self)
        result = _super._action_done()
        obj_stock_quant = self.env["stock.quant"]
        for move in self:
            if move.date_backdating:
                move.write({"date": move.date_backdating})
                for move_line in move.move_line_ids:
                    move_line.write(
                        {
                            "date": move.date_backdating,
                        }
                    )
                    obj_stock_quant._update_available_quantity(
                        product_id=move_line.product_id,
                        location_id=move_line.location_id,
                        quantity=move_line.product_qty,
                        lot_id=move_line.lot_id,
                        package_id=move_line.package_id,
                        owner_id=move_line.owner_id,
                        in_date=move.date_backdating,
                    )
        return result

    @api.multi
    def _account_entry_move(self):
        context = self._context.copy()
        if self.date_backdating:
            ctx = {
                "force_period_date": self.date_backdating,
            }
            context.update(ctx)
        return super(StockMove, self.with_context(context))._account_entry_move()
