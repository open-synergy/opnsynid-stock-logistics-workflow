# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class StockInvoiceOnshipping(models.TransientModel):
    _inherit = "stock.invoice.onshipping"

    @api.model
    def _default_stock_picking_id(self):
        active_ids = self._context.get("active_ids", [])
        if len(active_ids) > 0:
            return active_ids[0]
        else:
            return False

    stock_picking_id = fields.Many2one(
        string="Stock Picking",
        comodel_name="stock.picking",
        default=lambda self: self._default_stock_picking_id(),
    )
    allowed_invoice_journal_ids = fields.Many2many(
        string="Allowed Invoice Journals",
        comodel_name="account.journal",
        related="stock_picking_id.picking_type_id.allowed_invoice_journal_ids",
    )

    @api.onchange("stock_picking_id")
    def onchange_journal_id(self):
        self.journal_id = False
        if self.stock_picking_id:
            picking = self.stock_picking_id
            if picking.picking_type_id:
                picking_type = picking.picking_type_id
                if picking_type.default_invoice_journal_id:
                    self.journal_id = picking_type.default_invoice_journal_id
