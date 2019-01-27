# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, _
from openerp.exceptions import Warning as UserError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.model
    def _create_extra_moves(self, picking):
        if not picking.picking_type_id.allow_unexpected_product_transfer:
            str_msg = _("Not allowed to make unexpected product transfer")
            raise UserError(str_msg)
        _super = super(StockPicking, self)
        return _super._create_extra_moves(picking)
