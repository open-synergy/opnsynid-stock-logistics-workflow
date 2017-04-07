# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api
from openerp.addons.stock import stock_move


@api.model
def _push_apply(self, moves):
    obj_push = self.env["stock.location.path"]
    for move in moves:
        if move._check_push_allowed():
            rules = move._find_push_rule()
            if rules:
                obj_push._apply(rules[0], move)

    return True


class StockMoveMonkeypatch(models.TransientModel):
    _name = "stock.move.monkeypatch"
    _description = "Stock Move Monkeypatch"

    def _register_hook(self, cr):
        stock_move._push_apply = _push_apply
        return super(StockMoveMonkeypatch, self)._register_hook(cr)
