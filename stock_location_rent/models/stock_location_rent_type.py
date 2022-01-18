# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class StockLocationRentType(models.Model):
    _name = "stock.location_rent_type"
    _description = "Stock Location Rent Type"

    name = fields.Char(
        string="Rent Type",
        required=True,
    )
    code = fields.Char(
        string="Code",
        required=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    note = fields.Text(
        string="Note",
    )
    sequence_id = fields.Many2one(
        string="Sequence",
        comodel_name="ir.sequence",
        company_dependent=True,
    )
    allowed_location_ids = fields.Many2many(
        string="Allowed Location",
        comodel_name="stock.location",
        relation="rel_stock_location_rent_type_location",
        column1="type_id",
        column2="location_id",
    )
    allowed_yearly_pricelist_ids = fields.Many2many(
        string="Allowed Yearly Pricelist",
        comodel_name="product.pricelist",
        relation="rel_stock_location_rent_type_pricelist_yearly",
        column1="type_id",
        column2="pricelist_id",
    )
    allowed_monthly_pricelist_ids = fields.Many2many(
        string="Allowed Monthly Pricelist",
        comodel_name="product.pricelist",
        relation="rel_stock_location_rent_type_pricelist_monthly",
        column1="type_id",
        column2="pricelist_id",
    )
    allowed_daily_pricelist_ids = fields.Many2many(
        string="Allowed Daily Pricelist",
        comodel_name="product.pricelist",
        relation="rel_stock_location_rent_type_pricelist_daily",
        column1="type_id",
        column2="pricelist_id",
    )
    confirm_grp_ids = fields.Many2many(
        string="Allow To Confirm",
        comodel_name="res.groups",
        relation="rel_stock_location_rent_type_confirm",
        column1="type_id",
        column2="group_id",
    )
    finish_grp_ids = fields.Many2many(
        string="Allow To Finish",
        comodel_name="res.groups",
        relation="rel_stock_location_rent_type_finish",
        column1="type_id",
        column2="group_id",
    )
    terminate_grp_ids = fields.Many2many(
        string="Allow To Terminate",
        comodel_name="res.groups",
        relation="rel_stock_location_rent_type_terminate",
        column1="type_id",
        column2="group_id",
    )
    cancel_grp_ids = fields.Many2many(
        string="Allow To Cancel",
        comodel_name="res.groups",
        relation="rel_stock_location_rent_type_cancel",
        column1="type_id",
        column2="group_id",
    )
    restart_grp_ids = fields.Many2many(
        string="Allow To Restart",
        comodel_name="res.groups",
        relation="rel_stock_location_rent_type_restart",
        column1="type_id",
        column2="group_id",
    )
    restart_validation_grp_ids = fields.Many2many(
        string="Allow To Restart Validation",
        comodel_name="res.groups",
        relation="rel_stock_location_rent_type_restart_validation",
        column1="type_id",
        column2="group_id",
    )
