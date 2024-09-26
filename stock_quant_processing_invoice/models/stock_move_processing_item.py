# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from openerp.tools.safe_eval import safe_eval as eval


class StockMoveProcessingItem(models.Model):
    _name = "stock.move_processing_item"
    _description = "Stock Move Processing Item"

    name = fields.Char(
        string="Processing Item",
        required=True,
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        required=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    note = fields.Text(
        string="Note",
    )
    quantity_computation_code = fields.Text(
        string="Python Code for Quantity Computation",
        required=True,
        default="result = 1.0",
    )
    uom_computation_code = fields.Text(
        string="Python Code for UoM Computation",
        required=True,
        default="result = False",
    )

    @api.multi
    def _get_quantity(self, move, quant):
        self.ensure_one()
        result = 0.0
        localdict = self._get_quantity_localdict(move, quant)
        try:
            eval(self.quantity_computation_code,
                 localdict, mode="exec", nocopy=True)
            result = localdict["result"]
        # pylint: disable=locally-disabled, do-not-use-bare-except
        except:
            result = 0.0
        return result

    @api.multi
    def _get_quantity_localdict(self, move, quant):
        return {
            "env": self.env,
            "move": move,
            "quant": quant,
        }

    @api.multi
    def _get_uom_id(self, move, quant):
        self.ensure_one()
        localdict = self._get_uom_localdict(move, quant)
        try:
            eval(self.uom_computation_code,
                 localdict, mode="exec", nocopy=True)
            result = localdict["result"]
        # pylint: disable=locally-disabled, do-not-use-bare-except
        except:
            result = False
        return result

    @api.multi
    def _get_uom_localdict(self, move, quant):
        return {
            "env": self.env,
            "move": move,
            "quant": quant,
        }
