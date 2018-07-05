# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields, SUPERUSER_ID


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.multi
    @api.depends(
        "picking_type_id.invoice_group_ids",
    )
    def _compute_policy(self):
        super(StockPicking, self)._compute_policy()
        user_id = self.env.user.id
        for picking in self:
            picking_type = picking.picking_type_id
            if user_id == SUPERUSER_ID or not picking_type:
                picking.invoice_ok = True
                continue

            picking.invoice_ok =\
                self._button_picking_account_policy(
                    picking_type, 'invoice_ok')

    @api.model
    def _button_picking_account_policy(
        self, picking_type, button_type
    ):
        user = self.env.user
        group_ids = user.groups_id.ids
        button_group_ids = []

        if button_type == 'invoice_ok':
            button_group_ids =\
                picking_type.invoice_group_ids.ids

        if button_group_ids:
            if (set(button_group_ids) & set(group_ids)):
                result = True
            else:
                result = False
        else:
            result = True
        return result

    invoice_ok = fields.Boolean(
        string="Can Invoice",
        compute="_compute_policy",
        store=False,
    )
