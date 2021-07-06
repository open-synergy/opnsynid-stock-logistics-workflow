# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ProductCategory(models.Model):
    _inherit = "product.category"

    lot_sequence_id = fields.Many2one(
        string="Lot Sequence",
        comodel_name="ir.sequence",
        company_dependent=True,
    )
