# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields, SUPERUSER_ID


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.multi
    @api.depends(
        "state",
        "picking_type_id.confirm_group_ids",
        "picking_type_id.force_group_ids",
        "picking_type_id.transfer_group_ids",
        "picking_type_id.return_group_ids",
        "picking_type_id.cancel_group_ids",
        "picking_type_id.unreserve_group_ids",
    )
    def _compute_policy(self):
        user_id = self.env.user.id
        for picking in self:
            picking_type = picking.picking_type_id
            if user_id == SUPERUSER_ID:
                picking.confirm_ok = True
                picking.force_ok = True
                picking.transfer_ok = True
                picking.return_ok = True
                picking.cancel_ok = True
                picking.unreserve_ok = True
                continue

            picking.confirm_ok =\
                self._button_policy(picking_type, 'confirm')
            picking.force_ok =\
                self._button_policy(picking_type, 'force')
            picking.transfer_ok =\
                self._button_policy(picking_type, 'transfer')
            picking.return_ok =\
                self._button_policy(picking_type, 'return')
            picking.cancel_ok =\
                self._button_policy(picking_type, 'cancel')
            picking.unreserve_ok =\
                self._button_policy(picking_type, 'unreserve')

    @api.model
    def _button_policy(self, picking_type, button_type):
        user = self.env.user
        group_ids = user.groups_id.ids
        button_group_ids = []

        if button_type == 'confirm':
            button_group_ids = picking_type.confirm_group_ids.ids
        elif button_type == 'force':
            button_group_ids = picking_type.force_group_ids.ids
        elif button_type == 'transfer':
            button_group_ids = picking_type.transfer_group_ids.ids
        elif button_type == 'return':
            button_group_ids = picking_type.return_group_ids.ids
        elif button_type == 'cancel':
            button_group_ids = picking_type.cancel_group_ids.ids
        elif button_type == 'unreserve':
            button_group_ids = picking_type.unreserve_group_ids.ids

        if button_group_ids:
            if (set(button_group_ids) & set(group_ids)):
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
    force_ok = fields.Boolean(
        string="Can Force Availability",
        compute="_compute_policy",
        store=False,
    )
    transfer_ok = fields.Boolean(
        string="Can Transfer",
        compute="_compute_policy",
        store=False,
    )
    return_ok = fields.Boolean(
        string="Can Return",
        compute="_compute_policy",
        store=False,
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
        store=False,
    )
    unreserve_ok = fields.Boolean(
        string="Can Unreserve",
        compute="_compute_policy",
        store=False,
    )
