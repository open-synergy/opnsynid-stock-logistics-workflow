# Copyright 2015-2016 Agile Business Group (<http://www.agilebg.com>)
# Copyright 2015 BREMSKERL-REIBBELAGWERKE EMMERLING GmbH & Co. KG
#    Author Marco Dieckhoff
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    @api.model
    def create(self, vals):
        move_id = vals["move_id"]
        move = self.env["stock.move"].browse([move_id])[0]
        if move.date_backdating and "date" in vals:
            vals["date"] = move.date_backdating
        return super(StockMoveLine, self).create(vals)

    @api.multi
    def write(self, vals):
        for ml in self:
            if "date" in vals and ml.move_id and ml.move_id.date_backdating:
                vals["date"] = ml.move_id.date_backdating
            super(StockMoveLine, ml).write(vals)
