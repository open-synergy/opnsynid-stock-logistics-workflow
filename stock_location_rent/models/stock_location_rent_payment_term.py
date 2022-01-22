# -*- coding: utf-8 -*-
# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError


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

    @api.depends(
        "invoice_id",
        "rent_id.state",
    )
    def _compute_state(self):
        for record in self:
            if record.rent_id.state in ["draft", "confirm"]:
                state = "draft"
            elif record.rent_id.state in ["start", "finish"]:
                if record.invoice_id:
                    state = "invoiced"
                else:
                    state = "uninvoiced"
            elif record.rent_id.state == "terminate":
                if record.invoice_id:
                    state = "invoiced"
                else:
                    state = "terminated"
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
            ("terminated", "Terminated"),
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
        self.ensure_one()
        rent = self.rent_id
        obj_account_invoice = self.env["account.invoice"]
        invoice = obj_account_invoice.create(self._prepare_invoice_data())
        self.write(
            {
                "invoice_id": invoice.id,
            }
        )
        for detail in rent.detail_ids:
            detail._create_invoice_line(invoice, self.date_start, self.date_end)
        invoice.button_reset_taxes()
        return True

    @api.multi
    def _prepare_invoice_data(self):
        self.ensure_one()
        rent = self.rent_id
        partner = rent.partner_invoice_id or rent.partner_id
        return {
            "partner_id": partner.id,
            "date_invoice": self.date_invoice,
            "date_due": self.date_due,
            "journal_id": rent.receivable_journal_id.id,
            "account_id": rent.receivable_account_id.id,
            "currency_id": rent.currency_id.id,
            "origin": rent.name,
            "name": "Rental",
        }

    @api.multi
    def _delete_invoice(self):
        self.ensure_one()
        invoice = self.invoice_id
        if invoice.state == "draft":
            self.write({"invoice_id": False})
            invoice.unlink()
        else:
            msg_err = _("Only invoice with draft state can be deleted")
            raise UserError(msg_err)
        return True
