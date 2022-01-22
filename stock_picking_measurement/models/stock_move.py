# -*- coding: utf-8 -*-
# Copyright 2020 PT. Simetri Sinergi Indonesia
# Copyright 2020 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models
from openerp.addons import decimal_precision as dp


class StockMove(models.Model):
    _name = "stock.move"
    _inherit = "stock.move"

    @api.depends(
        "product_id",
        "product_qty",
    )
    @api.multi
    def _compute_measurement(self):
        for document in self:
            move_volume = move_net_weight = move_gross_weight = 0.0
            qty = document.product_qty
            if document.product_id:
                product = document.product_id
                move_volume = qty * product.volume
                move_net_weight = qty * product.weight_net
                move_gross_weight = qty * product.weight
            document.move_volume = move_volume
            document.move_net_weight = move_net_weight
            document.move_gross_weight = move_gross_weight

    move_volume = fields.Float(
        string="Volume",
        compute="_compute_measurement",
        store=True,
        digits_compute=dp.get_precision("Stock Volume"),
    )
    move_net_weight = fields.Float(
        string="Net Weight",
        compute="_compute_measurement",
        store=True,
        digits_compute=dp.get_precision("Stock Weight"),
    )
    move_gross_weight = fields.Float(
        string="Gross Weight",
        compute="_compute_measurement",
        store=True,
        digits_compute=dp.get_precision("Stock Weight"),
    )
