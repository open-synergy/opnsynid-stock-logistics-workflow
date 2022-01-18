# -*- coding: utf-8 -*-
# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from openerp.exceptions import Warning as UserError


class StockLocationRent(models.Model):
    _name = "stock.location_rent"
    _description = "Stock Location Rent"
    _inherit = [
        "mail.thread",
        "tier.validation",
        "base.sequence_document",
        "base.workflow_policy_object",
        "base.cancel.reason_common",
        "base.terminate.reason_common",
    ]
    _state_from = ["draft", "confirm"]
    _state_to = ["start"]

    @api.model
    def _default_company_id(self):
        return self.env.user.company_id.id

    @api.multi
    def _compute_policy(self):
        _super = super(StockLocationRent, self)
        _super._compute_policy()

    name = fields.Char(
        string="# Document",
        default="/",
        required=True,
        copy=False,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        required=True,
        default=lambda self: self._default_company_id(),
    )
    type_id = fields.Many2one(
        string="Rent Type",
        comodel_name="stock.location_rent_type",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    partner_id = fields.Many2one(
        string="Customer",
        comodel_name="res.partner",
        required=True,
        readonly=True,
        domain=[("parent_id", "=", False)],
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.multi
    @api.depends(
        "partner_id",
    )
    def _compute_allowed_partner_contact_ids(self):
        obj_res_partner = self.env["res.partner"]
        for document in self:
            res = document.partner_id
            if document.partner_id:
                criteria = [("parent_id", "=", document.partner_id.id)]
                partner_contact_ids = obj_res_partner.search(criteria).ids
                if partner_contact_ids:
                    res = partner_contact_ids
            document.allowed_partner_contact_ids = res

    allowed_partner_contact_ids = fields.Many2many(
        string="Allowed Partner Contacts",
        comodel_name="res.partner",
        compute="_compute_allowed_partner_contact_ids",
        store=False,
    )
    partner_contact_id = fields.Many2one(
        string="Contact",
        comodel_name="res.partner",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    partner_invoice_id = fields.Many2one(
        string="Invoice Address",
        comodel_name="res.partner",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    user_id = fields.Many2one(
        string="Sales Person",
        comodel_name="res.users",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    allowed_location_ids = fields.Many2many(
        string="Allowed Location",
        comodel_name="stock.location",
        related="type_id.allowed_location_ids",
    )
    allowed_yearly_pricelist_ids = fields.Many2many(
        string="Allowed Yearly Pricelist",
        comodel_name="product.pricelist",
        related="type_id.allowed_yearly_pricelist_ids",
    )
    allowed_monthly_pricelist_ids = fields.Many2many(
        string="Allowed Monthly Pricelist",
        comodel_name="product.pricelist",
        related="type_id.allowed_monthly_pricelist_ids",
    )
    allowed_daily_pricelist_ids = fields.Many2many(
        string="Allowed Daily Pricelist",
        comodel_name="product.pricelist",
        related="type_id.allowed_daily_pricelist_ids",
    )
    yearly_pricelist_id = fields.Many2one(
        string="Yearly Pricelist",
        comodel_name="product.pricelist",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    monthly_pricelist_id = fields.Many2one(
        string="Monthly Pricelist",
        comodel_name="product.pricelist",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    daily_pricelist_id = fields.Many2one(
        string="Daily Pricelist",
        comodel_name="product.pricelist",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date_start = fields.Date(
        string="Date Start",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date_end = fields.Date(
        string="Date End",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.multi
    @api.depends(
        "date_start",
        "date_end",
    )
    def _compute_period(self):
        for document in self:
            if document.date_start and document.date_end:
                start = datetime.strptime(document.date_start, "%Y-%m-%d")
                end = datetime.strptime(document.date_end, "%Y-%m-%d")
                document.yearly_period = relativedelta(end, start).years
                document.monthly_period = relativedelta(end, start).months
                document.daily_period = relativedelta(end, start).days

    yearly_period = fields.Integer(
        string="Yearly Period",
        compute="_compute_period",
        store=True,
    )
    monthly_period = fields.Integer(
        string="Monthly Period",
        compute="_compute_period",
        store=True,
    )
    daily_period = fields.Integer(
        string="Daily Period",
        compute="_compute_period",
        store=True,
    )
    detail_ids = fields.One2many(
        string="Details",
        comodel_name="stock.location_rent_detail",
        inverse_name="rent_id",
        copy=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    payment_term_ids = fields.One2many(
        string="Payment Terms",
        comodel_name="stock.location_rent_payment_term",
        inverse_name="rent_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.multi
    def _compute_allowed_receivable_journal_ids(self):
        for document in self:
            document.allowed_invoice_ids = []

    allowed_receivable_journal_ids = fields.Many2many(
        string="Allowed Receivable Journals",
        comodel_name="account.journal",
        compute="_compute_allowed_receivable_journal_ids",
        store=False,
    )
    receivable_journal_id = fields.Many2one(
        string="Receivable Journal",
        comodel_name="account.journal",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.multi
    def _compute_allowed_receivable_account_ids(self):
        for document in self:
            document.allowed_invoice_ids = []

    allowed_receivable_account_ids = fields.Many2many(
        string="Allowed Receivable Accounts",
        comodel_name="account.journal",
        compute="_compute_allowed_receivable_account_ids",
        store=False,
    )
    receivable_account_id = fields.Many2one(
        string="Receivable Account",
        comodel_name="account.account",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    note = fields.Text(
        string="Note",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("start", "Start"),
            ("finish", "Finish"),
            ("terminate", "Terminated"),
            ("cancel", "Cancelled"),
        ],
        copy=False,
        default="draft",
        required=True,
        readonly=True,
    )
    # Log Fields
    confirm_date = fields.Datetime(
        string="Confirm Date",
        readonly=True,
        copy=False,
    )
    confirm_user_id = fields.Many2one(
        string="Confirmed By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    start_date = fields.Datetime(
        string="Start Date",
        readonly=True,
        copy=False,
    )
    start_user_id = fields.Many2one(
        string="Start By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    finish_date = fields.Datetime(
        string="Finish Date",
        readonly=True,
        copy=False,
    )
    finish_user_id = fields.Many2one(
        string="Finished By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    cancel_date = fields.Datetime(
        string="Cancel Date",
        readonly=True,
        copy=False,
    )
    cancel_user_id = fields.Many2one(
        string="Cancelled By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )
    terminate_date = fields.Datetime(
        string="Terminate Date",
        readonly=True,
        copy=False,
    )
    terminate_user_id = fields.Many2one(
        string="Terminated By",
        comodel_name="res.users",
        readonly=True,
        copy=False,
    )

    # Policy Field
    confirm_ok = fields.Boolean(
        string="Can Confirm",
        compute="_compute_policy",
    )
    finish_ok = fields.Boolean(
        string="Can Done",
        compute="_compute_policy",
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
    )
    terminate_ok = fields.Boolean(
        string="Can Terminate",
        compute="_compute_policy",
    )
    restart_validation_ok = fields.Boolean(
        string="Can Restart Validation",
        compute="_compute_policy",
    )
    restart_ok = fields.Boolean(
        string="Can Restart",
        compute="_compute_policy",
    )

    @api.multi
    def action_confirm(self):
        for document in self:
            document.write(document._prepare_confirm_data())
            document.request_validation()

    @api.multi
    def action_start(self):
        for document in self:
            document.write(document._prepare_start_data())

    @api.multi
    def action_finish(self):
        for document in self:
            document.write(document._prepare_finish_data())

    @api.multi
    def action_cancel(self):
        for document in self:
            document.write(document._prepare_cancel_data())
            document.restart_validation()

    @api.multi
    def action_terminate(self):
        for document in self:
            document.write(document._prepare_terminate_data())

    @api.multi
    def action_restart(self):
        for document in self:
            document.write(document._prepare_restart_data())

    @api.multi
    def _prepare_confirm_data(self):
        self.ensure_one()
        return {
            "state": "confirm",
            "confirm_date": fields.Datetime.now(),
            "confirm_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_start_data(self):
        self.ensure_one()
        sequence = self._create_sequence()
        return {
            "state": "start",
            "name": sequence,
            "start_date": fields.Datetime.now(),
            "start_user_id": self.env.user.id,
            "finish_date": False,
            "finish_user_id": False,
        }

    @api.multi
    def _prepare_finish_data(self):
        self.ensure_one()
        return {
            "state": "finish",
            "finish_date": fields.Datetime.now(),
            "finish_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_cancel_data(self):
        self.ensure_one()
        return {
            "state": "cancel",
            "cancel_date": fields.Datetime.now(),
            "cancel_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_terminate_data(self):
        self.ensure_one()
        return {
            "state": "terminate",
            "terminate_date": fields.Datetime.now(),
            "terminate_user_id": self.env.user.id,
        }

    @api.multi
    def _prepare_restart_data(self):
        self.ensure_one()
        return {
            "state": "draft",
            "confirm_date": False,
            "confirm_user_id": False,
            "start_date": False,
            "start_user_id": False,
            "finish_date": False,
            "finish_user_id": False,
            "cancel_date": False,
            "cancel_user_id": False,
            "terminate_date": False,
            "terminate_user_id": False,
            "cancel_reason_id": False,
            "terminate_reason_id": False,
        }

    @api.multi
    def unlink(self):
        strWarning = _("You can only delete data on draft state")
        for document in self:
            if document.state != "draft":
                if not self.env.context.get("force_unlink", False):
                    raise UserError(strWarning)
        _super = super(StockLocationRent, self)
        _super.unlink()

    @api.multi
    def validate_tier(self):
        _super = super(StockLocationRent, self)
        _super.validate_tier()
        for document in self:
            if document.validated:
                document.action_start()

    @api.multi
    def restart_validation(self):
        _super = super(StockLocationRent, self)
        _super.restart_validation()
        for document in self:
            document.request_validation()

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            if record.name == "/":
                name = "*" + str(record.id)
            else:
                name = record.name
            result.append((record.id, name))
        return result

    @api.multi
    @api.constrains(
      "date_start",
      "date_end",
    )
    def _check_tanggal(self):
        for record in self:
            if record.date_start and record.date_end:
                if record.date_start > record.date_end:
                    msg_err = _("Date Start cannot be greater than Date End")
                    raise UserError(msg_err)
