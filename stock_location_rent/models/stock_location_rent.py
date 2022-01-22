# -*- coding: utf-8 -*-
# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime

from dateutil.relativedelta import relativedelta
from openerp import _, api, fields, models
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

    @api.depends("currency_id", "payment_term_period_id")
    def _compute_allowed_pricelist_ids(self):
        obj_pricelist = self.env["product.pricelist"]
        for record in self:
            result = []
            if (
                record.currency_id
                and record.payment_term_period_id
                and record.payment_term_period_id.allowed_pricelist_ids
            ):
                allowed_pricelists = record.payment_term_period_id.allowed_pricelist_ids
                criteria = [
                    ("currency_id", "=", record.currency_id.id),
                    ("id", "in", allowed_pricelists.ids),
                ]
                result = obj_pricelist.search(criteria)
            record.allowed_pricelist_ids = result

    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    allowed_pricelist_ids = fields.Many2many(
        string="Allowed Pricelist",
        comodel_name="product.pricelist",
        compute="_compute_allowed_pricelist_ids",
        store=False,
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
                delta_date = relativedelta(end, start)
                document.yearly_period = delta_date.years
                document.monthly_period = delta_date.months
                document.daily_period = delta_date.days

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

    @api.multi
    @api.depends(
        "type_id",
        "date_start",
        "date_end",
    )
    def _compute_allowed_payment_term_period_id(self):
        obj_payment_term_period = self.env["stock.location_rent_payment_term_period"]
        format = "%Y-%m-%d"
        for document in self:
            res = []
            if document.type_id and document.date_start and document.date_end:

                payment_term_period_ids = document.type_id.payment_term_period_ids

                lst_type = ["daily"]
                if document.daily_period == 0:
                    if document.monthly_period == 0:
                        lst_type += ["monthly", "yearly"]
                    else:
                        lst_type += ["monthly"]

                if lst_type:
                    criteria_payment_term = [
                        ("id", "in", payment_term_period_ids.ids),
                        ("type", "in", lst_type),
                    ]
                    payment_term_period_ids = obj_payment_term_period.search(
                        criteria_payment_term
                    )

                    if payment_term_period_ids:
                        for term_period in payment_term_period_ids:
                            if term_period.type == "yearly":
                                check_number = document.yearly_period
                            elif term_period.type == "monthly":
                                check_number = document.yearly_period * 12
                                check_number += document.monthly_period
                            elif term_period.type == "daily":
                                dt_start = datetime.strptime(
                                    document.date_start, format
                                )
                                dt_end = datetime.strptime(document.date_end, format)
                                check_number = (dt_end - dt_start).days
                            check_period_number = (
                                check_number % term_period.payment_term_period_number
                            )
                            if check_period_number == 0 and check_number != 0:
                                res.append(term_period.id)

            document.allowed_payment_term_period_id = res

    allowed_payment_term_period_id = fields.Many2many(
        string="Allowed Payment Term Period",
        comodel_name="stock.location_rent_payment_term_period",
        compute="_compute_allowed_payment_term_period_id",
        store=False,
    )
    payment_term_period_id = fields.Many2one(
        string="Payment Term Period",
        comodel_name="stock.location_rent_payment_term_period",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    payment_term_period_number = fields.Integer(
        string="Payment Term Period Number",
        related="payment_term_period_id.payment_term_period_number",
        readonly=True,
    )
    invoice_method = fields.Selection(
        string="Invoice Method",
        selection=[
            ("advance", "Advance"),
            ("arear", "Arear"),
        ],
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date_invoice_offset = fields.Integer(
        string="Date Invoice Offset",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.multi
    @api.depends(
        "payment_term_period_id",
        "date_start",
        "date_end",
    )
    def _compute_invoice_number(self):
        for document in self:
            invoice_number = 0
            if (
                document.payment_term_period_id
                and document.date_start
                and document.date_end
            ):
                payment_term_period_number = (
                    document.payment_term_period_id.payment_term_period_number
                )
                period_type = document.payment_term_period_id.type
                format = "%Y-%m-%d"

                dt_start = datetime.strptime(document.date_start, format)
                dt_end = datetime.strptime(document.date_end, format)
                rent_days = (dt_end - dt_start).days
                if period_type == "yearly":
                    conv_days = rent_days / 365
                elif period_type == "monthly":
                    r_months = relativedelta(dt_end, dt_start)
                    conv_days = r_months.months + (12 * r_months.years)
                else:
                    conv_days = rent_days / 1
                invoice_number = conv_days / payment_term_period_number
            document.invoice_number = invoice_number

    invoice_number = fields.Integer(
        string="Invoice Number",
        compute="_compute_invoice_number",
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

    @api.depends(
        "amount_before_tax",
        "amount_tax",
        "amount_after_tax",
    )
    @api.multi
    def _compute_total_invoice(self):
        for document in self:
            document.total_invoice_before_tax = (
                document.amount_before_tax * document.invoice_number
            )
            document.total_invoice_tax = document.amount_tax * document.invoice_number
            document.total_invoice_after_tax = (
                document.amount_after_tax * document.invoice_number
            )

    total_invoice_before_tax = fields.Float(
        string="Total Invoice Before Tax",
        compute="_compute_total_invoice",
        store=True,
    )
    total_invoice_tax = fields.Float(
        string="Total Invoice Tax",
        compute="_compute_total_invoice",
        store=True,
    )
    total_invoice_after_tax = fields.Float(
        string="Total Invoice After Tax",
        compute="_compute_total_invoice",
        store=True,
    )

    @api.depends(
        "detail_ids.amount_before_tax",
        "detail_ids.amount_tax",
        "detail_ids.amount_after_tax",
    )
    @api.multi
    def _compute_amount(self):
        for document in self:
            amount_before_tax = 0.0
            amount_tax = 0.0
            amount_after_tax = 0.0
            if document.detail_ids:
                for detail in document.detail_ids:
                    amount_before_tax += detail.amount_before_tax
                    amount_tax += detail.amount_tax
                    amount_after_tax += detail.amount_after_tax
            document.amount_before_tax = amount_before_tax
            document.amount_tax = amount_tax
            document.amount_after_tax = amount_after_tax

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
    payment_term_id = fields.Many2one(
        string="Invoice Payment Term",
        comodel_name="account.payment.term",
        required=True,
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
    )
    allowed_receivable_journal_ids = fields.Many2many(
        string="Allowed Receivable Journals",
        comodel_name="account.journal",
        related="type_id.allowed_receivable_journal_ids",
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
    allowed_receivable_account_ids = fields.Many2many(
        string="Allowed Receivable Accounts",
        comodel_name="account.account",
        related="type_id.allowed_receivable_account_ids",
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

    @api.onchange(
        "date_start",
        "date_end",
    )
    def onchange_date_payment_term_period_id(self):
        if self.date_start or self.date_end:
            self.payment_term_period_id = False

    @api.onchange(
        "payment_term_period_id",
    )
    def onchange_pricelist_id(self):
        self.pricelist_id = False

    @api.multi
    def action_create_payment_schedule(self):
        for document in self:
            document._delete_payment_schedule()
            document._create_payment_schedule()

    @api.multi
    def _delete_payment_schedule(self):
        self.ensure_one()
        if self.payment_term_ids:
            for document in self.payment_term_ids:
                invoice_id = document.invoice_id
                document.write({"invoice_id": False})
                invoice_id.unlink()
            self.payment_term_ids.unlink()

    @api.multi
    def _create_payment_schedule(self):
        self.ensure_one()
        obj_payment_term = self.env["stock.location_rent_payment_term"]
        date_start = self.date_start
        for _period_num in range(1, self.invoice_number + 1):
            date_end = self._get_payment_schedule_date_end(date_start)
            date_invoice = self._get_payment_schedule_date_invoice(date_start)
            date_due = self._get_payment_schedule_date_due(date_invoice)
            data = {
                "rent_id": self.id,
                "date_start": date_start,
                "date_end": date_end,
                "date_invoice": date_invoice,
                "date_due": date_due,
            }
            obj_payment_term.create(data)
            date_start = date_end

    @api.multi
    def _get_payment_schedule_date_due(self, date_invoice):
        self.ensure_one()
        res = date_invoice
        obj_account_payment_term = self.env["account.payment.term"]
        payment_term = obj_account_payment_term.browse(self.payment_term_id.id)
        payment_term_list = payment_term.compute(value=1, date_ref=date_invoice)[0]
        if payment_term_list:
            res = max(line[0] for line in payment_term_list)
        return res

    @api.multi
    def _get_payment_schedule_date_invoice(self, date):
        self.ensure_one()
        if self.invoice_method == "advance":
            factor = relativedelta(days=(self.date_invoice_offset * -1))
        else:
            factor = relativedelta(days=self.date_invoice_offset)

        dt_start = fields.Date.from_string(date)
        date_start = dt_start + factor
        return fields.Date.to_string(date_start)

    @api.multi
    def _get_payment_schedule_date_start(self, date_end):
        self.ensure_one()

        dt_end = fields.Date.from_string(date_end)
        date_start = dt_end + relativedelta(days=1)
        return fields.Date.to_string(date_start)

    @api.multi
    def _get_payment_schedule_date_end(self, date):
        self.ensure_one()

        if self.payment_term_period_id.type == "daily":
            add = relativedelta(
                days=self.payment_term_period_id.payment_term_period_number
            )
        elif self.payment_term_period_id.type == "monthly":
            add = relativedelta(
                months=self.payment_term_period_id.payment_term_period_number
            )
        else:
            add = relativedelta(
                years=self.payment_term_period_id.payment_term_period_number
            )
        dt_date = fields.Date.from_string(date)
        date_end = dt_date + add
        return fields.Date.to_string(date_end)

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

    @api.constrains("state", "payment_term_ids")
    def _check_number_of_payment_term(self):
        msg_err = _("No payment terms")
        for record in self:
            if record.state == "confirm" and len(record.payment_term_ids) == 0:
                raise UserError(msg_err)

    @api.constrains(
        "state",
    )
    def _check_payment_term_criteria(self):
        msg_err = _("Please cancel all payment term invoices")
        for record in self:
            num_not_allowed = record._get_not_allowed_to_be_cancelled_payment_term()
            if record.state == "cancel" and num_not_allowed > 0:
                raise UserError(msg_err)

    @api.multi
    def _prepare_not_allowed_tobe_cancelled_payment_term_domain(self):
        self.ensure_one()
        return [
            ("rent_id", "=", self.id),
            (
                "state",
                "=",
                "invoiced",
            ),
        ]

    @api.multi
    def _get_not_allowed_to_be_cancelled_payment_term(self):
        self.ensure_one()
        dom = self._prepare_not_allowed_tobe_cancelled_payment_term_domain()
        obj_period = self.env["stock.location_rent_payment_term"]
        return obj_period.search_count(dom)
