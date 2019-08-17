# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class StockMoveProcessingInvoice(models.Model):
    _name = "stock.move_processing_invoice"
    _description = "Stock Move Processing Invoice"

    @api.multi
    @api.depends(
        "price_unit",
        "quantity",
    )
    def _compute_subtotal(self):
        for document in self:
            document.subtotal = document.price_unit * document.quantity

    move_id = fields.Many2one(
        string="Stock Move",
        comodel_name="stock.move",
        required=True,
        ondelete="restrict",
    )
    picking_id = fields.Many2one(
        string="# Picking",
        comodel_name="stock.picking",
        related="move_id.picking_id",
        store=True,
    )
    quant_id = fields.Many2one(
        string="Quant",
        comodel_name="stock.quant",
        required=True,
        ondelete="restrict",
    )
    item_id = fields.Many2one(
        string="Processing Item",
        comodel_name="stock.move_processing_item",
        required=True,
        ondelete="restrict",
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        required=True,
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        required=True,
    )
    invoice_id = fields.Many2one(
        string="# Invoice",
        comodel_name="account.invoice",
        related="invoice_line_id.invoice_id",
        store=True,
    )
    invoice_line_id = fields.Many2one(
        string="Invoice Line",
        comodel_name="account.invoice.line",
    )
    price_unit = fields.Float(
        string="Price",
        required=True,
    )
    quantity = fields.Float(
        string="Qty.",
        required=True,
    )
    uom_id = fields.Many2one(
        string="UoM",
        comodel_name="product.uom",
        required=True,
    )
    tax_ids = fields.Many2many(
        string="Taxes",
        comodel_name="account.tax",
        relation="rel_stock_move_processing_invoice_2_tax",
        column1="processing_id",
        column2="tax_id",
    )
    subtotal = fields.Float(
        string="Sub Total",
        compute="_compute_subtotal",
        store=True,
    )
