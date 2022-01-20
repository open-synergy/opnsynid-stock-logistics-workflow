# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class StockLocation(models.Model):
    _inherit = "stock.location"

    rent_product_id = fields.Many2one(
        string="Product Location Rent",
        comodel_name="product.product",
    )
    income_account_id = fields.Many2one(
        string="Income Account",
        comodel_name="account.account",
    )
    deffered_revenue_account_id = fields.Many2one(
        string="Deffered Revenue Account",
        comodel_name="account.account",
    )
