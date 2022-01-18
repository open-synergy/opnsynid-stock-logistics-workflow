# -*- coding: utf-8 -*-
# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class StockLocationRentDetail(models.Model):
    _name = "stock.location_rent_detail"
    _description = "Stock Location Rent Detail"

    rent_id = fields.Many2one(
        string="# Rent",
        comodel_name="stock.location_rent",
        required=True,
        ondelete="cascade",
    )
    location_id = fields.Many2one(
        string="Location",
        comodel_name="stock.location",
        required=True,
    )
    account_id = fields.Many2one(
        string="Account",
        comodel_name="account.account",
        required=True,
    )
    yearly_pricelist_id = fields.Many2one(
        string="Yearly Pricelist",
        comodel_name="product.pricelist",
        required=True,
    )
    monthly_pricelist_id = fields.Many2one(
        string="Monthly Pricelist",
        comodel_name="product.pricelist",
        required=True,
    )
    daily_pricelist_id = fields.Many2one(
        string="Daily Pricelist",
        comodel_name="product.pricelist",
        required=True,
    )
    yearly_period = fields.Integer(
        string="Yearly Period",
    )
    monthly_period = fields.Integer(
        string="Monthly Period",
    )
    daily_period = fields.Integer(
        string="Daily Period",
    )
    yearly_price_unit = fields.Float(
        string="Yearly Price Unit",
        required=True,
    )
    monthly_price_unit = fields.Float(
        string="Monthly Price Unit",
        required=True,
    )
    daily_price_unit = fields.Float(
        string="Daily Price Unit",
        required=True,
    )
    tax_ids = fields.Many2many(
        string="Taxes",
        comodel_name="account.tax",
        relation="rel_stock_location_rent_detail_2_tax",
        column1="rent_detail_id",
        column2="tax_id",
    )
    detail_ids = fields.One2many(
        string="Details",
        comodel_name="stock.location_rent_payment_term_detail",
        inverse_name="detail_id",
    )

    @api.depends(
        "yearly_period",
        "monthly_period",
        "daily_period",
        "yearly_price_unit",
        "monthly_price_unit",
        "daily_price_unit",
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
