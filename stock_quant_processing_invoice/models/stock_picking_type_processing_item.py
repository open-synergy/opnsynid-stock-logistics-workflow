# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class StockPickingTypeProcessingItem(models.Model):
    _name = "stock.picking_type_processing_item"
    _description = "Stock Picking Type Processing Item"

    type_id = fields.Many2one(
        string="Picking Type",
        comodel_name="stock.picking.type",
        required=True,
        ondelete="cascade",
    )
    item_id = fields.Many2one(
        string="Processing Item",
        comodel_name="stock.move_processing_item",
        required=True,
    )
    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
    )
