# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def create(self, vals):
        if self._context.get("force_period_date"):
            vals["date"] = self._context["force_period_date"]
        return super(AccountMove, self).create(vals)
