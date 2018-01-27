# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api


class StockPickingWave(models.Model):
    _inherit = "stock.picking.wave"

    @api.onchange("type_id")
    def onchange_delivery_address_ids(self):
        self.delivery_address_ids = False
        if self.type_id:
            if self.type_id.delivery_address_ids:
                self.delivery_address_ids = self.type_id.delivery_address_ids

    @api.onchange("type_id")
    def onchange_picking_type_ids(self):
        self.picking_type_ids = False
        if self.type_id:
            if self.type_id.allowed_picking_type_ids:
                self.picking_type_ids = self.type_id.allowed_picking_type_ids

    @api.onchange("date_start", "date_end", "type_id")
    def onchange_creation_date_start(self):
        self.creation_date_start = False
        if self.type_id and self.date_start and self.date_end:
            self.creation_date_start = self.type_id._compute_date(
                "creation_date_start", self.date_start, self.date_end)

    @api.onchange("date_start", "date_end", "type_id")
    def onchange_creation_date_end(self):
        self.creation_date_end = False
        if self.type_id and self.date_start and self.date_end:
            self.creation_date_end = self.type_id._compute_date(
                "creation_date_end", self.date_start, self.date_end)

    @api.onchange("date_start", "date_end", "type_id")
    def onchange_schedule_date_start(self):
        self.schedule_date_start = False
        if self.type_id and self.date_start and self.date_end:
            self.scheduled_date_start = self.type_id._compute_date(
                "scheduled_date_start", self.date_start, self.date_end)

    @api.onchange("date_start", "date_end", "type_id")
    def onchange_schedule_date_end(self):
        self.schedule_date_end = False
        if self.type_id and self.date_start and self.date_end:
            self.scheduled_date_end = self.type_id._compute_date(
                "scheduled_date_end", self.date_start, self.date_end)
