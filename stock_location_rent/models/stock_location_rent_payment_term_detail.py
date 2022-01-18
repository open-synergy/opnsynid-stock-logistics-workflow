# -*- coding: utf-8 -*-
# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class StockLocationRentPaymentTermDetail(models.Model):
    _name = "stock.location_rent_payment_term_detail"
    _description = "Stock Location Rent Payment Term Detail"

    detail_id = fields.Many2one(
        string="# Rent",
        comodel_name="stock.location_rent_detail",
        required=True,
        ondelete="cascade",
    )
    payment_term_id = fields.Many2one(
        string="Payment Term",
        comodel_name="stock.location_rent_payment_term",
    )
    date_start = fields.Date(
        string="Date Start",
        required=True,
    )
    date_end = fields.Date(
        string="Date End",
        required=True,
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        required=True,
    )
    price_unit = fields.Float(
        string="Price Unit",
        required=True,
    )
    tax_ids = fields.Many2many(
        string="Taxes",
        comodel_name="account.tax",
        relation="rel_stock_location_rent_payment_term_detail_2_tax",
        column1="payment_term_detail_id",
        column2="tax_id",
    )
    @api.depends(
        "price_unit",
        "tax_ids",
    )
    @api.multi
    def _compute_amount(self):
        for document in self:
            document.amount_before_tax = 0.0
            document.amount_tax = 0.0
            document.amount_after_tax = 0.0

    amount_before_tax = fields.Float(
        string="Amount Before Tax",
        compute="_compute_amount",
        store=True,
    )
    amount_tax = fields.Float(
        string="Amount Tax",
        compute="_compute_amount",
        store=True,
    )
    amount_after_tax = fields.Float(
        string="Amount After Tax",
        compute="_compute_amount",
        store=True,
    )
