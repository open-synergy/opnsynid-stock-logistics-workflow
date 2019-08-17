# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from openerp.tools.safe_eval import safe_eval as eval


class StockFulfillmentItem(models.Model):
    _name = "stock.fulfillment_item"
    _description = "Stock Fulfillment Item"

    name = fields.Char(
        string="Fulfillment Item",
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
    applicable_on = fields.Selection(
        string="Applicable On",
        selection=[
            ("picking", "Picking"),
            ("move", "Move"),
            ("quant", "Quant"),
        ],
        required=True,
    )
    sequence_id = fields.Many2one(
        string="Sequence",
        comodel_name="ir.sequence",
        company_dependent=True,
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
    def _get_quantity(self, document):
        self.ensure_one()
        result = 0.0
        localdict = self._get_quantity_localdict(document)
        try:
            eval(self.quantity_computation_code,
                 localdict, mode="exec", nocopy=True)
            result = localdict["result"]
        # pylint: disable=locally-disabled, do-not-use-bare-except
        except:
            result = 0.0
        return result

    @api.multi
    def _get_quantity_localdict(self, document):
        return {
            "env": self.env,
            "self": self,
            "document": document,
        }

    @api.multi
    def _get_uom_id(self, document):
        self.ensure_one()
        localdict = self._get_uom_localdict(document)
        try:
            eval(self.uom_computation_code,
                 localdict, mode="exec", nocopy=True)
            result = localdict["result"]
        # pylint: disable=locally-disabled, do-not-use-bare-except
        except:
            result = False
        return result

    @api.multi
    def _get_uom_localdict(self, document):
        return {
            "env": self.env,
            "self": self,
            "document": document,
        }

    @api.multi
    def _prepare_fulfillment_service(self, currency, price, qty, uom_id):
        self.ensure_one()
        return {
            "item_id": self.id,
            "price_unit": price,
            "currency_id": currency.id,
            "quantity": qty,
            "uom_id": uom_id,
            "tax_ids": [
                (6, 0, self.product_id.taxes_id.ids),
            ],
        }
