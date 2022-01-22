# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    lot_sequence_id = fields.Many2one(
        string="Lot Sequence",
        comodel_name="ir.sequence",
        company_dependent=True,
    )
