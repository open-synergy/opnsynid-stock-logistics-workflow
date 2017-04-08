# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.multi
    def _prepare_init_domain(self):
        self.ensure_one()
        domains = super(StockMove, self)._prepare_init_domain()
        if self.picking_type_id:
            domain = [
                "|",
                ("picking_type_ids", "=", False),
                ("picking_type_ids.id", "in", [self.picking_type_id.id]),
            ]
            domains += domain
        return domains
