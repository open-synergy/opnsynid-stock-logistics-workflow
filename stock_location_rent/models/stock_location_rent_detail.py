# -*- coding: utf-8 -*-
# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models, _
from openerp.exceptions import Warning as UserError


class StockLocationRentDetail(models.Model):
    _name = "stock.location_rent_detail"
    _description = "Stock Location Rent Detail"

    rent_id = fields.Many2one(
        string="# Rent",
        comodel_name="stock.location_rent",
        ondelete="cascade",
    )
    allowed_location_ids = fields.Many2many(
        string="Allowed Location",
        comodel_name="stock.location",
        related="rent_id.type_id.allowed_location_ids",
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
    invoice_method = fields.Selection(
        string="Invoice Method",
        related="rent_id.invoice_method"
    )

    @api.model
    def _default_pricelist_id(self):
        return self.rent_id.pricelist_id.id

    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
        default=lambda self: self._default_pricelist_id(),
        required=True,
    )
    price_unit = fields.Float(
        string="Price Unit",
        required=True,
    )
    tax_ids = fields.Many2many(
        string="Taxes",
        comodel_name="account.tax",
        relation="rel_stock_location_rent_detail_2_tax",
        column1="rent_detail_id",
        column2="tax_id",
    )

    @api.depends(
        "price_unit",
        "tax_ids",
    )
    @api.multi
    def _compute_amount(self):
        for document in self:
            tax_comp = document.tax_ids.compute_all(
                price_unit=document.price_unit,
                quantity=1.0,
            )
            document.amount_before_tax = tax_comp["total"]
            document.amount_tax = (tax_comp["total_included"] - tax_comp["total"])
            document.amount_after_tax = tax_comp["total_included"]

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

    @api.multi
    def _create_invoice_line(self, invoice, date_start, date_end):
        self.ensure_one()
        obj_account_invoice_line = self.env["account.invoice.line"]
        obj_account_invoice_line.create(
            self._prepare_invoice_line(invoice, date_start, date_end)
        )

    @api.multi
    def _prepare_invoice_line(self, invoice, date_start, date_end):
        self.ensure_one()
        name = "Rent for {} from {} to {}".format(
            self.location_id.name,
            date_start,
            date_end
        )
        return {
            "invoice_id": invoice.id,
            "name": name,
            "account_id": self.account_id.id,
            "price_unit": self.price_unit,
            "product_id": self.location_id.rent_product_id.id,
            "invoice_line_tax_id": [(6, 0, self.tax_ids.ids)],
        }

    @api.onchange(
        "location_id",
        "invoice_method",
    )
    def onchange_account_id(self):
        if self.location_id:
            if self.rent_id.invoice_method == "advance":
                self.account_id = self.location_id.deffered_revenue_account_id
            if self.rent_id.invoice_method == "arear":
                self.account_id = self.location_id.income_account_id

    @api.onchange(
        "pricelist_id",
    )
    def onchange_price_unit(self):
        price_unit = 0.0
        if self.pricelist_id:
            if not self.location_id.rent_product_id:
                msg_err = _("Product location rent not found")
                raise UserError(msg_err)
            price_unit = self.pricelist_id.price_get(
                prod_id=self.location_id.rent_product_id.id,
                qty=1.0,
            )[self.pricelist_id.id]
        self.price_unit = price_unit
