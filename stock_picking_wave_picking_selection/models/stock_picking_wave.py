# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _
from openerp.exceptions import Warning as UserError


class StockPickingWave(models.Model):
    _inherit = "stock.picking.wave"

    delivery_address_ids = fields.Many2many(
        string="Delivery Address",
        comodel_name="res.partner",
        relation="picking_wave_partner_rel",
        column1="wave_id",
        column2="partner_id",
    )
    picking_type_ids = fields.Many2many(
        string="Picking Type",
        comodel_name="stock.picking.type",
        relation="picking_wave_picking_type_rel",
        column1="wave_id",
        column2="picking_type_id",
    )
    scheduled_date_start = fields.Datetime(
        string="Scheduled Date Start"
    )
    scheduled_date_end = fields.Datetime(
        string="Scheduled Date End"
    )
    creation_date_start = fields.Datetime(
        string="Creation Date Start"
    )
    creation_date_end = fields.Datetime(
        string="Creation Date End"
    )

    @api.constrains(
        "scheduled_date_start", "scheduled_date_end")
    def _check_scheduled_date(self):
        strWarning = _(
            "Scheduled Date Start must be greater than Scheduled Date End")
        if self.scheduled_date_start and self.scheduled_date_end:
            if self.scheduled_date_start > self.scheduled_date_end:
                raise UserError(strWarning)

    @api.constrains(
        "creation_date_start", "creation_date_end")
    def _check_creation_date(self):
        strWarning = _(
            "Creation Date Start must be greater than Creation Date End")
        if self.creation_date_start and self.creation_date_end:
            if self.creation_date_start > self.creation_date_end:
                raise UserError(strWarning)

    @api.multi
    def _prepare_picking_search(self):
        self.ensure_one()
        criteria = []

        scheduled_date_start = self.scheduled_date_start
        scheduled_date_end = self.scheduled_date_end
        creation_date_start = self.creation_date_start
        creation_date_end = self.creation_date_end
        delivery_address_ids = self.delivery_address_ids
        picking_type_ids = self.picking_type_ids

        if scheduled_date_start:
            criteria.append(
                ("min_date", ">=", scheduled_date_start)
            )
        if scheduled_date_end:
            criteria.append(
                ("min_date", "<=", scheduled_date_end)
            )
        if creation_date_start:
            criteria.append(
                ("date", ">=", creation_date_start)
            )
        if creation_date_end:
            criteria.append(
                ("date", "<=", creation_date_end)
            )
        if delivery_address_ids:
            criteria.append(
                ("delivery_address_id", "in", delivery_address_ids.ids)
            )
        if picking_type_ids:
            criteria.append(
                ("picking_type_id", "in", picking_type_ids.ids)
            )
        return criteria

    @api.multi
    def button_search_pickings(self):
        obj_stock_picking = self.env["stock.picking"]

        criteria = self._prepare_picking_search()
        criteria.append(
            ("wave_id", "=", False)
        )
        criteria.append(
            ("state", "not in", ("cancel", "done"))
        )
        picking_ids = obj_stock_picking.search(criteria)
        if picking_ids:
            self.picking_ids = [(6, 0, picking_ids.ids)]
        else:
            self.picking_ids = [(6, 0, [])]
