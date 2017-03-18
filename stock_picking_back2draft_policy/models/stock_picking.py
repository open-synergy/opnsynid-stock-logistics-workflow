# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.multi
    @api.depends(
        "picking_type_id.back2draft_group_ids",
    )
    def _compute_policy(self):
        super(StockPicking, self)._compute_policy()
        obj_picking_type = self.env["stock.picking.type"]
        for picking in self:
            picking.back2draft_ok = False
            picking_id = self.env.context.get("default_picking_type_id", False)
            if not picking_id:
                continue
            picking_type = obj_picking_type.browse([picking_id])[0]
            picking.back2draft_ok = self._back2draft_policy(picking_type)

    @api.model
    def _back2draft_policy(self, picking_type):
        result = False
        user = self.env.user
        back2draft_group_ids = picking_type.back2draft_group_ids.ids
        group_ids = user.groups_id.ids
        if not picking_type.back2draft_group_ids.ids:
            result = True
        else:
            if (set(back2draft_group_ids) & set(group_ids)):
                result = True
        return result

    back2draft_ok = fields.Boolean(
        string="Can Back to Draft",
        compute="_compute_policy",
        store=False,
    )
