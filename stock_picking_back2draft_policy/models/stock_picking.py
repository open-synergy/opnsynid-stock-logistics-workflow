# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields, SUPERUSER_ID


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.multi
    @api.depends(
        "picking_type_id.back2draft_group_ids",
    )
    def _compute_policy(self):
        super(StockPicking, self)._compute_policy()
        user_id = self.env.user.id
        for picking in self:
            picking_type = picking.picking_type_id
            if user_id == SUPERUSER_ID or not picking_type:
                picking.back2draft_ok = True
                continue

            picking.back2draft_ok =\
                self._button_back2draft_policy(
                    picking_type, 'back2draft_ok')

    @api.model
    def _button_back2draft_policy(self, picking_type, button_type):
        user = self.env.user
        group_ids = user.groups_id.ids
        button_group_ids = []

        if button_type == 'back2draft_ok':
            button_group_ids = picking_type.back2draft_group_ids.ids

        if button_group_ids:
            if (set(button_group_ids) & set(group_ids)):
                result = True
            else:
                result = False
        else:
            result = True
        return result

    back2draft_ok = fields.Boolean(
        string="Can Back to Draft",
        compute="_compute_policy",
        store=False,
    )
