# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models


class ProcurementOrder(models.Model):
    _inherit = "procurement.order"

    @api.multi
    def _find_procurement_pull_rules(self, domain):
        self.ensure_one()
        obj_rule = self.env["procurement.rule"]
        dom = self._prepare_procurement_pull_rule_domain(domain)
        if self.move_dest_id and self.move_dest_id.picking_type_id:
            pick_type = self.move_dest_id.picking_type_id
            dom1 = dom + [("picking_type_ids", "in", [pick_type.id])]
            rules = obj_rule.search(dom1, order="route_sequence, sequence")
            if not rules:
                return obj_rule.search(dom, order="route_sequence, sequence")
        else:
            return obj_rule.search(dom, order="route_sequence, sequence")

    @api.multi
    def _find_product_pull_rules(self, domain):
        self.ensure_one()
        obj_rule = self.env["procurement.rule"]
        dom = self._prepare_product_pull_rule_domain(domain)
        if self.move_dest_id and self.move_dest_id.picking_type_id:
            pick_type = self.move_dest_id.picking_type_id
            dom1 = dom + [("picking_type_ids", "in", [pick_type.id])]
            rules = obj_rule.search(dom1, order="route_sequence, sequence")
            if not rules:
                return obj_rule.search(dom, order="route_sequence, sequence")
        else:
            return obj_rule.search(dom, order="route_sequence, sequence")

    @api.multi
    def _find_warehouse_pull_rules(self, domain):
        self.ensure_one()
        obj_rule = self.env["procurement.rule"]
        dom = self._prepare_warehouse_pull_rule_domain(domain)
        if self.move_dest_id and self.move_dest_id.picking_type_id:
            pick_type = self.move_dest_id.picking_type_id
            dom1 = dom + [("picking_type_ids", "in", [pick_type.id])]
            rules = obj_rule.search(dom1, order="route_sequence, sequence")
            if not rules:
                return obj_rule.search(dom, order="route_sequence, sequence")
        else:
            return obj_rule.search(dom, order="route_sequence, sequence")

    @api.multi
    def _find_global_pull_rules(self, domain):
        self.ensure_one()
        obj_rule = self.env["procurement.rule"]
        dom = self._prepare_global_pull_rule_domain(domain)
        if self.move_dest_id and self.move_dest_id.picking_type_id:
            pick_type = self.move_dest_id.picking_type_id
            dom1 = dom + [("picking_type_ids", "in", [pick_type.id])]
            rules = obj_rule.search(dom1, order="route_sequence, sequence")
            if not rules:
                return obj_rule.search(dom, order="route_sequence, sequence")
        else:
            return obj_rule.search(dom, order="route_sequence, sequence")
