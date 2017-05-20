# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.multi
    def _check_push_allowed(self):
        self.ensure_one()
        result = False
        domain = self._prepare_allowed_domain()
        obj_move = self.env["stock.move"]
        if obj_move.search_count(domain) == 1:
            result = True
        return result

    @api.multi
    def _prepare_allowed_domain(self):
        self.ensure_one()
        domain = [
            ("id", "=", self.id),
            ("move_dest_id", "=", False),
            ("origin_returned_move_id", "=", False),
        ]
        return domain

    @api.multi
    def _prepare_init_domain(self):
        self.ensure_one()
        domain = [
            ("location_from_id", "=", self.location_dest_id.id),
        ]
        return domain

    @api.multi
    def _find_push_rule(self):
        obj_rule = self.env["stock.location.path"]
        domain = self._prepare_init_domain()
        rules = self._find_product_related_push_rule(domain)
        if len(rules) == 0:
            rules = self._find_wh_related_push_rule(domain)
            if rules == 0:
                domain += [("route_id", "=", False)]
                rules = obj_rule.search(
                    domain, order="sequence")
        if len(rules) > 0:
            rule = rules[0]
        else:
            rule = False
        return rule

    @api.multi
    def _find_product_related_push_rule(self, domain):
        self.ensure_one()
        obj_rule = self.env["stock.location.path"]
        routes = self.product_id.route_ids + \
            self.product_id.categ_id.total_route_ids
        dom = domain + [("route_id", "in", routes.ids)]
        return obj_rule.search(dom)

    @api.multi
    def _find_wh_related_push_rule(self, domain):
        self.ensure_one()
        obj_rule = self.env["stock.location.path"]
        if self.warehouse_id:
            routes = self.warehouse_id.route_ids
        elif self.picking_type_id and self.picking_type_id.warehouse_id:
            routes = self.picking_type_id.warehouse_id.route_ids
        else:
            routes = self.env["stock.location.route"]
        dom = domain + [("route_id", "in", routes.ids)]
        return obj_rule.search(dom)
