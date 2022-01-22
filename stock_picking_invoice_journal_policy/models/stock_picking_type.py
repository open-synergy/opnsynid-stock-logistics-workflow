# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    allowed_invoice_journal_ids = fields.Many2many(
        string="Allowed Invoice Journals",
        comodel_name="account.journal",
        relation="rel_stock_picking_type_2_invoice_journal",
        column1="stock_picking_id",
        column2="journal_id",
    )
    default_invoice_journal_id = fields.Many2one(
        string="Default Invoice Journal",
        comodel_name="account.journal",
    )
