# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import SUPERUSER_ID, api, fields, models


class StockPickingWave(models.Model):
    _inherit = "stock.picking.wave"

    @api.multi
    @api.depends(
        "state",
        "type_id.confirm_group_ids",
        "type_id.done_group_ids",
        "type_id.cancel_group_ids",
    )
    def _compute_policy(self):
        user_id = self.env.user.id
        for wave in self:
            wave_type = wave.type_id
            if user_id == SUPERUSER_ID or not wave_type:
                wave.confirm_ok = True
                wave.done_ok = True
                wave.cancel_ok = True
                continue

            wave.confirm_ok = self._button_policy(wave_type, "confirm")
            wave.done_ok = self._button_policy(wave_type, "done")
            wave.cancel_ok = self._button_policy(wave_type, "cancel")

    @api.model
    def _button_policy(self, picking_wave_type, button_type):
        user = self.env.user
        group_ids = user.groups_id.ids
        button_group_ids = []

        if button_type == "confirm":
            button_group_ids = picking_wave_type.confirm_group_ids.ids
        elif button_type == "done":
            button_group_ids = picking_wave_type.done_group_ids.ids
        elif button_type == "cancel":
            button_group_ids = picking_wave_type.cancel_group_ids.ids

        if button_group_ids:
            if set(button_group_ids) & set(group_ids):
                result = True
            else:
                result = False
        else:
            result = True
        return result

    confirm_ok = fields.Boolean(
        string="Can Confirm",
        compute="_compute_policy",
        store=False,
    )
    done_ok = fields.Boolean(
        string="Can Done",
        compute="_compute_policy",
        store=False,
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
        store=False,
    )
