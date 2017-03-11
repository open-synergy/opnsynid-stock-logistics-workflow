# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.multi
    @api.depends(
        "picking_type_id.invoice_group_ids",
    )
    def _compute_policy(self):
        super(StockPicking, self)._compute_policy()
        obj_picking_type = self.env["stock.picking.type"]
        for picking in self:
            picking.invoice_ok = False
            picking_id = self.env.context.get("default_picking_type_id", False)
            if not picking_id:
                continue
            picking_type = obj_picking_type.browse([picking_id])[0]
            picking.invoice_ok = self._invoice_policy(picking_type)

    @api.model
    def _invoice_policy(self, picking_type):
        result = False
        user = self.env.user
        invoice_group_ids = picking_type.invoice_group_ids.ids
        group_ids = user.groups_id.ids
        if not picking_type.invoice_group_ids.ids:
            result = True
        else:
            if (set(invoice_group_ids) & set(group_ids)):
                result = True
        return result

    invoice_ok = fields.Boolean(
        string="Can Invoice",
        compute="_compute_policy",
        store=False,
    )
