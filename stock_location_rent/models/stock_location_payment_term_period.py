# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import _, api, fields, models
from openerp.exceptions import Warning as UserError, ValidationError


class StockLocationRentPaymentTermPeriod(models.Model):
    _name = "stock.location_rent_payment_term_period"
    _description = "Stock Location Rent Payment Term Period"

    name = fields.Char(
        string="Payment Term Period",
        required=True,
    )
    code = fields.Char(
        string="Code",
        required=True,
    )
    type = fields.Selection(
        string="Period Type",
        selection=[
            ("daily", "Daily"),
            ("monthly", "Monthly"),
            ("yearly", "Yearly"),
        ],
        required=True,
    )
    payment_term_period_number = fields.Integer(
        string="Payment Term Period Number",
        required=True,
        default=1,
    )
    allowed_pricelist_ids = fields.Many2many(
        string="Allowed Pricelist",
        comodel_name="product.pricelist",
        relation="rel_stock_location_rent_payment_term_period_2_pricelist",
        column1="payment_term_period_id",
        column2="pricelist_id",
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    note = fields.Text(
        string="Note",
    )

    @api.constrains(
        "pricelist_id",
        "allowed_pricelist_ids"
    )
    def _check_default_pricelist(self):
        error_msg = _("Default pricelist must available on allowed pricelist")
        if self.pricelist_id:
            if self.pricelist_id.id not in self.allowed_pricelist_ids.ids:
                raise ValidationError(error_msg)