# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models
from openerp.addons.stock import procurement


@api.model
def _search_suitable_rule(self, procurement, domain):
    domain = procurement._prepare_init_domain(domain)
    rules = procurement._find_procurement_pull_rules(domain)
    if not rules:
        rules = procurement._find_product_pull_rules(domain)
        if not rules:
            if procurement.warehouse_id:
                rules = procurement._find_warehouse_pull_rules(domain)
            if not rules:
                rules = procurement._find_global_pull_rules(domain)
    return rules


class ProcurementOrderMonkeypatch(models.TransientModel):
    _name = "procurement.order.monkeypatch"
    _description = "Procurement Order Monkeypatch"

    def _register_hook(self, cr):
        procurement._search_suitable_rule = _search_suitable_rule
        return super(ProcurementOrderMonkeypatch, self)._register_hook(cr)
