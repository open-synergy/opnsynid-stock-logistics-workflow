# Copyright 2015-2016 Agile Business Group (<http://www.agilebg.com>)
# Copyright 2015 BREMSKERL-REIBBELAGWERKE EMMERLING GmbH & Co. KG
#    Author Marco Dieckhoff
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.multi
    def _action_done(self):
        _super = super(StockMove, self)
        result = _super._action_done()
        for move in self:
            if move.inventory_id.backdate:
                move.write({"date": move.inventory_id.backdate})
        return result
