# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.multi
    def _prepare_allowed_domain(self):
        self.ensure_one()
        domains = super(StockMove, self)._prepare_allowed_domain()
        for domain in domains:
            if domain[0] == "origin_returned_move_id":
                domains.remove(domain)
        return domains
