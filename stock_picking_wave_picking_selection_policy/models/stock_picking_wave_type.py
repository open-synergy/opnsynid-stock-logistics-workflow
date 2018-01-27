# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime


class StockPickingWaveType(models.Model):
    _inherit = "stock.picking_wave_type"

    delivery_address_ids = fields.Many2many(
        string="Delivery Address",
        comodel_name="res.partner",
        relation="rel_wave_type_2_partner",
        column1="wave_type_id",
        column2="partner_id",
    )
    creation_date_start_anchor = fields.Selection(
        string="Compute Creation Date Start From",
        selection=[
            ("date_start", "Date Start"),
            ("date_end", "Date End"),
        ],
    )
    creation_date_start_offset = fields.Float(
        string="Creation Date Start Offset",
    )
    creation_date_end_anchor = fields.Selection(
        string="Compute Creation Date End From",
        selection=[
            ("date_start", "Date Start"),
            ("date_end", "Date End"),
        ],
    )
    creation_date_end_offset = fields.Float(
        string="Creation Date End Offset",
    )
    scheduled_date_start_anchor = fields.Selection(
        string="Compute Schedule Date Start From",
        selection=[
            ("date_start", "Date Start"),
            ("date_end", "Date End"),
        ],
    )
    scheduled_date_start_offset = fields.Float(
        string="Schedule Date Start Offset",
    )
    scheduled_date_end_anchor = fields.Selection(
        string="Compute Schedule Date End From",
        selection=[
            ("date_start", "Date Start"),
            ("date_end", "Date End"),
        ],
    )
    scheduled_date_end_offset = fields.Float(
        string="Schedule Date End Offset",
    )

    @api.multi
    def _compute_date(self, field_to_compute, date_start, date_end):
        self.ensure_one()
        dt_start = datetime.strptime(date_start, "%Y-%m-%d %H:%M:%S")
        dt_end = datetime.strptime(date_end, "%Y-%m-%d %H:%M:%S")
        anchor_field_name = field_to_compute + "_anchor"
        offset_field_name = field_to_compute + "_offset"

        if not getattr(self, anchor_field_name):
            return False

        if getattr(self, anchor_field_name) == "date_start":
            anchor = dt_start
        elif getattr(self, anchor_field_name) == "date_end":
            anchor = dt_end

        hour_offset = int(getattr(self, offset_field_name))
        minute_offset = int((getattr(self, offset_field_name) % 1) * 60.0)

        result = anchor + \
            relativedelta(hours=+hour_offset, minutes=+minute_offset)
        return result.strftime("%Y-%m-%d %H:%M:%Y")
