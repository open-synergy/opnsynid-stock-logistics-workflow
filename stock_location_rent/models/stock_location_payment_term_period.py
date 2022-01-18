# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


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
        ]
    )
    payment_term_period_number = fields.Integer(
        string="Payment Term Period Number",
        required=True,
        default=1,
    )
    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
        required=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    note = fields.Text(
        string="Note",
    )
