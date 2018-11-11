# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    force_ok = fields.Boolean(
        string="Can Force Validation",
        compute="_compute_policy",
        store=False,
        readonly=True,
    )
