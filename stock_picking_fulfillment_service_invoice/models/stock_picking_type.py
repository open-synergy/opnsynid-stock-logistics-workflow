# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"
    _name = "stock.picking.type"

    fulfillment_item_ids = fields.One2many(
        string="Fulfillment Items",
        comodel_name="stock.picking_type_fulfillment_item",
        inverse_name="type_id",
    )
