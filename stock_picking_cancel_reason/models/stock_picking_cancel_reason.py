# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class StockPickingCancelReason(models.Model):
    _name = "stock.picking.cancel.reason"
    _description = "Stock Picking Cancel Reason"

    name = fields.Char(string="Reason", required=True)
    description = fields.Text(string="Description")
    active = fields.Boolean(string="Active", default=True)
