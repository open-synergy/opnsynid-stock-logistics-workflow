# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    date_backdating = fields.Datetime(
        string="Actual Movement Date",
        compute="_compute_date_backdating",
        inverse="_inverse_set_move_lines_date_backdating",
        store=True,
        readonly=True,
        states={
            "assigned": [
                ("readonly", False),
            ],
        },
    )

    @api.depends(
        "move_lines",
        "move_lines.date_backdating",
    )
    def _compute_date_backdating(self):
        for record in self:
            if record.move_lines:
                record.date_backdating = record.move_lines[0].date_backdating

    def _inverse_set_move_lines_date_backdating(self):
        for picking in self:
            picking.move_lines.write({"date_backdating": picking.date_backdating})

    def _action_done(self):
        _super = super(StockPicking, self)
        result = _super._action_done()
        if self.date_backdating:
            self.write({"date_done": self.date_backdating})
        return result
