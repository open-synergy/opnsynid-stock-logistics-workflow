# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class StockPicking(models.Model):
    _inherit = "stock.picking"

    cancel_reason_id = fields.Many2one(
        comodel_name="stock.picking.cancel.reason",
        string="Reason for cancellation",
        readonly=True,
        ondelete="restrict"
    )
