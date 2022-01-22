# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    default_move_procure_method = fields.Selection(
        string="Default Procure Method",
        selection=[
            ("make_to_stock", "Default: Take From Stock"),
            ("make_to_order", "Advanced: Apply Procurement Rules"),
        ],
    )
