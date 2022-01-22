# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models
from openerp.exceptions import Warning as UserError
from openerp.tools.translate import _


class StockPickingWave(models.Model):
    _inherit = "stock.picking.wave"

    date_start = fields.Datetime(
        string="Date Start",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    date_end = fields.Datetime(
        string="Date End",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.constrains("date_start", "date_end")
    def _check_wave_interval(self):
        strWarning1 = _("Date End must be greater than Date Start")
        strWarning2 = _("Date Start required")
        strWarning3 = _("Date End required")

        if self.date_start and not self.date_end:
            raise UserError(strWarning3)

        if not self.date_start and self.date_end:
            raise UserError(strWarning2)

        if self.date_start and self.date_end:
            if self.date_start > self.date_end:
                raise UserError(strWarning1)
