# -*- coding: utf-8 -*-
# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class StockLocationRentPaymentTerm(models.Model):
    _name = "stock.location_rent_payment_term"
    _description = "Stock Location Rent Payment Term"

    rent_id = fields.Many2one(
        string="# Rent",
        comodel_name="stock.location_rent",
        required=True,
        ondelete="cascade",
    )
    date_start = fields.Date(
        string="Date Start",
        required=True,
    )
    date_end = fields.Date(
        string="Date End",
        required=True,
    )
    date_invoice = fields.Date(
        string="Date Invoice",
        required=True,
    )
    date_due = fields.Date(
        string="Date Due",
        required=True,
    )
    invoice_id = fields.Many2one(
        string="# Invoice",
        comodel_name="account.invoice",
        readonly=True,
        ondelete="restrict",
    )
    detail_ids = fields.One2many(
        string="Details",
        comodel_name="stock.location_rent_payment_term_detail",
        inverse_name="payment_term_id",
    )
    @api.depends(
        "detail_ids.price_unit",
        "detail_ids.tax_ids",
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

    @api.depends(
        "invoice_id",
        "rent_id.state",
    )
    def _compute_state(self):
        for record in self:
            if record.rent_id.state in ["draft", "confirm"]:
                state = "draft"
            elif record.rent_id.state in ["start", "finish", "terminate"]:
                if record.invoice_id:
                    state = "invoiced"
                else:
                    state = "uninvoiced"
            else:
                state = "cancelled"
            record.state = state

    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("uninvoiced", "Uninvoiced"),
            ("invoiced", "Invoiced"),
            ("cancelled", "Cancelled"),
        ],
        compute="_compute_state",
        store=True,
    )

    @api.multi
    def action_create_invoice(self):
        for record in self:
            record._create_invoice()

    @api.multi
    def action_delete_invoice(self):
        for record in self:
            record._delete_invoice()

    @api.multi
    def _create_invoice(self):
        # self.ensure_one()
        # invoice = self.env["account.invoice"].create(self._prepare_invoice_data())
        # self.write(
        #     {
        #         "invoice_id": invoice.id,
        #     }
        # )
        # for detail in self.detail_ids:
        #     detail._create_invoice_line()
        # invoice.button_reset_taxes()
        return True

    # @api.multi
    # def _prepare_invoice_data(self):
    #     self.ensure_one()
    #     contract = self.contract_id
    #     partner = contract.partner_invoice_id or contract.partner_id
    #     return {
    #         "partner_id": partner.id,
    #         "date_invoice": False,  # TODO
    #         "journal_id": journal.id,
    #         "account_id": account.id,
    #         "currency_id": contract.currency_id.id,
    #         "origin": contract.name,
    #         "name": contract.title,
    #     }

    @api.multi
    def _delete_invoice(self):
        # self.ensure_one()
        # invoice = self.invoice_id
        # self.detail_ids.write({"invoice_line_id": False})
        # self.write(
        #     {
        #         "invoice_id": False,
        #     }
        # )
        # invoice.unlink()
        return True
