# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class StockCreateFulfillmentInvoice(models.TransientModel):
    _name = "stock.create_fulfillment_invoice"
    _description = "Create Fulfillment Invoice"

    @api.multi
    @api.depends(
        "currency_id",
    )
    def _compute_allowed_journal_ids(self):
        obj_journal = self.env["account.journal"]
        for wizard in self:
            if wizard.currency_id:
                if wizard.currency_id == self.env.user.company_id.currency_id:
                    currency_id = False
                else:
                    currency_id = wizard.currency_id.id

                criteria = [
                    ("currency", "=", currency_id),
                    ("type", "=", "sale"),
                ]
                wizard.allowed_journal_ids = obj_journal.search(criteria).ids
            else:
                wizard.allowed_journal_ids = []

    @api.model
    def _default_fulfillment_service_ids(self):
        item_ids = self.env.context.get("active_ids", [])
        return [(6, 0, item_ids)]

    date_invoice = fields.Date(
        string="Date Invoice",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        required=True,
    )
    allowed_journal_ids = fields.Many2many(
        string="Allowed Journals",
        comodel_name="account.journal",
        compute="_compute_allowed_journal_ids",
        store=False,
    )
    journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
        required=True,
        domain=[
            ("type", "=", "sale"),
        ],
    )
    fulfillment_service_ids = fields.Many2many(
        string="Fulfillment Services",
        comodel_name="stock.fulfillment_service",
        default=lambda self: self._default_fulfillment_service_ids(),
        relation="rel_wiz_create_fulfillment_invoice_2_service",
        column1="wiz_id",
        column2="service_id",
    )

    @api.multi
    def action_create_invoice(self):
        self.ensure_one()
        obj_invoice = self.env["account.invoice"]
        obj_invoice_line = self.env["account.invoice.line"]
        invoices = {}
        for line in self.fulfillment_service_ids.filtered(
                lambda r: r.currency_id.id == self.currency_id.id and
                not r.invoice_line_id):
            invoice_id = invoices.get(line.partner_id.id, False)
            if not invoice_id:
                invoice = obj_invoice.create(
                    self._prepare_invoice(line.partner_id))
                invoices[line.partner_id.id] = invoice.id
            inv_line = obj_invoice_line.create(
                self._prepare_invoice_line(invoice, line))
            line.write({"invoice_line_id": inv_line.id})

    @api.multi
    def _prepare_invoice(self, partner):
        self.ensure_one()
        return {
            "partner_id": partner.id,
            "date_invoice": self.date_invoice,
            "journal_id": self.journal_id.id,
            "account_id": partner.property_account_receivable.id,
        }

    @api.multi
    def _prepare_invoice_line(self, invoice, fulfillment_service):
        self.ensure_one()
        account_id = fulfillment_service.item_id.product_id.\
            _get_processing_account_id()
        return {
            "invoice_id": invoice.id,
            "name": fulfillment_service.name,
            "product_id": fulfillment_service.item_id.product_id.id,
            "account_id": account_id,
            "quantity": fulfillment_service.quantity,
            "uos_id": fulfillment_service.uom_id.id,
            "price_unit": fulfillment_service.price_unit,
            "invoice_line_tax_id": fulfillment_service.tax_ids.ids,
        }
