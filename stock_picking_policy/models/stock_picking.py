# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields


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
        obj_picking_type = self.env["stock.picking.type"]
        for picking in self:
            picking.confirm_ok = picking.force_ok = picking.transfer_ok = \
                picking.return_ok = picking.cancel_ok = \
                picking.unreserve_ok = False
            picking_id = self.env.context.get("default_picking_type_id", False)
            if not picking_id:
                continue
            picking_type = obj_picking_type.browse([picking_id])[0]
            picking.confirm_ok = self._confirm_policy(picking_type)
            picking.force_ok = self._force_policy(picking_type)
            picking.transfer_ok = self._transfer_policy(picking_type)
            picking.return_ok = self._return_policy(picking_type)
            picking.cancel_ok = self._cancel_policy(picking_type)
            picking.unreserve_ok = self._unreserve_policy(picking_type)

    @api.model
    def _confirm_policy(self, picking_type):
        result = False
        user = self.env.user
        confirm_group_ids = picking_type.confirm_group_ids.ids
        group_ids = user.groups_id.ids
        if not picking_type.confirm_group_ids.ids:
            result = True
        else:
            if (set(confirm_group_ids) & set(group_ids)):
                result = True
        return result

    @api.model
    def _force_policy(self, picking_type):
        result = False
        user = self.env.user
        force_group_ids = picking_type.force_group_ids.ids
        group_ids = user.groups_id.ids
        if not picking_type.force_group_ids.ids:
            result = True
        else:
            if (set(force_group_ids) & set(group_ids)):
                result = True
        return result

    @api.model
    def _transfer_policy(self, picking_type):
        result = False
        user = self.env.user
        transfer_group_ids = picking_type.transfer_group_ids.ids
        group_ids = user.groups_id.ids
        if not picking_type.transfer_group_ids.ids:
            result = True
        else:
            if (set(transfer_group_ids) & set(group_ids)):
                result = True
        return result

    @api.model
    def _return_policy(self, picking_type):
        result = False
        user = self.env.user
        return_group_ids = picking_type.return_group_ids.ids
        group_ids = user.groups_id.ids
        if not picking_type.return_group_ids.ids:
            result = True
        else:
            if (set(return_group_ids) & set(group_ids)):
                result = True
        return result

    @api.model
    def _cancel_policy(self, picking_type):
        result = False
        user = self.env.user
        cancel_group_ids = picking_type.cancel_group_ids.ids
        group_ids = user.groups_id.ids
        if not picking_type.cancel_group_ids.ids:
            result = True
        else:
            if (set(cancel_group_ids) & set(group_ids)):
                result = True
        return result

    @api.model
    def _unreserve_policy(self, picking_type):
        result = False
        user = self.env.user
        unreserve_group_ids = picking_type.unreserve_group_ids.ids
        group_ids = user.groups_id.ids
        if not picking_type.unreserve_group_ids.ids:
            result = True
        else:
            if (set(unreserve_group_ids) & set(group_ids)):
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
