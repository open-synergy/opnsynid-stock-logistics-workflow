# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    @api.model
    def _default_name(self):
        return "/"

    name = fields.Char(
        string="Serial Number",
        required=True,
        help="Unique Serial Number",
        default=lambda self: self._default_name(),
    )

    @api.model
    def create(self, values):
        product_id = values["product_id"]
        if values["name"] == "/":
            values["name"] = self._create_sequence(product_id)
        _super = super(StockProductionLot, self)
        return _super.create(values)

    @api.model
    def _create_sequence(self, product_id):
        sequence = self._get_sequence(product_id)
        name = self.env["ir.sequence"].\
            next_by_id(sequence.id)
        return name

    @api.model
    def _get_sequence(self, product_id):
        obj_product = self.env["product.product"]
        product = obj_product.browse([product_id])[0]
        if product.lot_sequence_id:
            return product.lot_sequence_id
        else:
            return self.env.ref("stock.sequence_production_lots")
