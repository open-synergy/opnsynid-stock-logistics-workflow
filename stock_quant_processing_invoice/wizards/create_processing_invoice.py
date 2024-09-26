# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class StockCreateProcessingInvoice(models.TransientModel):
    _name = "stock.create_processing_invoice"
    _description = "Create Processing Invoice"

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
    def _default_processing_item_ids(self):
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
    processing_item_ids = fields.Many2many(
        string="Processing Items",
        comodel_name="stock.move_processing_invoice",
        default=lambda self: self._default_processing_item_ids(),
        relation="rel_wiz_create_processing_invoice_2_item",
        column1="wiz_id",
        column2="item_id",
    )

    @api.multi
    def action_create_invoice(self):
        self.ensure_one()
        obj_invoice = self.env["account.invoice"]
        obj_invoice_line = self.env["account.invoice.line"]
        invoices = {}
        for line in self.processing_item_ids.filtered(
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
    def _prepare_invoice_line(self, invoice, processing_line):
        self.ensure_one()
        account_id = processing_line.item_id.product_id.\
            _get_processing_account_id()
        return {
            "invoice_id": invoice.id,
            "name": processing_line.item_id.name,
            "product_id": processing_line.item_id.product_id.id,
            "account_id": account_id,
            "quantity": processing_line.quantity,
            "uos_id": processing_line.uom_id.id,
            "price_unit": processing_line.price_unit,
            "invoice_line_tax_id": processing_line.tax_ids.ids,
        }
