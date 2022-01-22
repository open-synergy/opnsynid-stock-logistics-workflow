# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models


class ProcurementOrder(models.Model):
    _inherit = "procurement.order"

    @api.multi
    def _prepare_init_domain(self, domain):
        self.ensure_one()
        return domain

    @api.multi
    def _find_procurement_pull_rules(self, domain):
        self.ensure_one()
        obj_rule = self.env["procurement.rule"]
        dom = self._prepare_procurement_pull_rule_domain(domain)
        return obj_rule.search(dom, order="route_sequence, sequence")

    @api.multi
    def _prepare_procurement_pull_rule_domain(self, domain):
        self.ensure_one()
        dom = domain + [("route_id", "in", self.route_ids.ids)]
        return dom

    @api.multi
    def _find_product_pull_rules(self, domain):
        self.ensure_one()
        obj_rule = self.env["procurement.rule"]
        dom = self._prepare_product_pull_rule_domain(domain)
        return obj_rule.search(dom, order="route_sequence, sequence")

    @api.multi
    def _prepare_product_pull_rule_domain(self, domain):
        self.ensure_one()
        routes = self.product_id.route_ids + self.product_id.categ_id.total_route_ids
        dom = domain + [("route_id", "in", routes.ids)]
        return dom

    @api.multi
    def _find_warehouse_pull_rules(self, domain):
        self.ensure_one()
        obj_rule = self.env["procurement.rule"]
        dom = self._prepare_warehouse_pull_rule_domain(domain)
        return obj_rule.search(dom, order="route_sequence, sequence")

    @api.multi
    def _prepare_warehouse_pull_rule_domain(self, domain):
        self.ensure_one()
        routes = self.warehouse_id.route_ids
        dom = domain + [("route_id", "in", routes.ids)]
        return dom

    @api.multi
    def _find_global_pull_rules(self, domain):
        self.ensure_one()
        obj_rule = self.env["procurement.rule"]
        dom = self._prepare_global_pull_rule_domain(domain)
        return obj_rule.search(dom, order="route_sequence, sequence")

    @api.multi
    def _prepare_global_pull_rule_domain(self, domain):
        self.ensure_one()
        dom = domain + [("route_id", "=", False)]
        return dom
