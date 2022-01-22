# -*- coding: utf-8 -*-
# Copyright 2020 PT. Simetri Sinergi Indonesia
# Copyright 2020 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models
from openerp.addons import decimal_precision as dp


class StockPicking(models.Model):
    _name = "stock.picking"
    _inherit = "stock.picking"

    @api.depends(
        "move_lines",
        "move_lines.move_volume",
        "move_lines.move_net_weight",
        "move_lines.move_gross_weight",
    )
    @api.multi
    def _compute_measurement(self):
        for document in self:
            picking_volume = picking_net_weight = picking_gross_weight = 0.0
            for move in document.move_lines:
                picking_volume += move.move_volume
                picking_gross_weight += move.move_gross_weight
                picking_net_weight += move.move_net_weight

            document.picking_volume = picking_volume
            document.picking_net_weight = picking_net_weight
            document.picking_gross_weight = picking_gross_weight

    picking_volume = fields.Float(
        string="Volume",
        compute="_compute_measurement",
        store=True,
        digits_compute=dp.get_precision("Stock Volume"),
    )
    picking_net_weight = fields.Float(
        string="Net Weight",
        compute="_compute_measurement",
        store=True,
        digits_compute=dp.get_precision("Stock Weight"),
    )
    picking_gross_weight = fields.Float(
        string="Gross Weight",
        compute="_compute_measurement",
        store=True,
        digits_compute=dp.get_precision("Stock Weight"),
    )
