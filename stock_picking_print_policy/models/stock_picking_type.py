# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class StockPickingTypePrintPolicy(models.Model):
    _name = "stock.picking_type_print_policy"
    _description = "Picking Type Print Policy"

    @api.depends(
        "type_id.window_action_id",
        "type_id.window_action_id.view_ids",
    )
    @api.multi
    def _compute_original_view(self):
        for policy in self:
            policy.original_view_id = False
            if not policy.type_id.window_action_id:
                continue
            criteria = [
                ("act_window_id", "=", policy.type_id.window_action_id.id),
                ("view_mode", "=", "form"),
            ]
            self.original_view_id = \
                self.env["ir.actions.act_window.view"].search(
                    criteria, limit=1)[0].view_id.id

    name = fields.Char(
        string="Button Label",
        required=True,
    )
    type_id = fields.Many2one(
        string="Picking Type",
        comodel_name="stock.picking.type",
    )
    report_id = fields.Many2one(
        string="Print",
        comodel_name="ir.actions.report.xml",
        required=True,
        ondelete="restrict",
    )
    view_id = fields.Many2one(
        string="View",
        comodel_name="ir.ui.view",
        readonly=True,
        ondelete="restrict",
    )
    original_view_id = fields.Many2one(
        string="Original View",
        comodel_name="ir.ui.view",
        readonly=True,
        compute="_compute_original_view",
    )
    group_ids = fields.Many2many(
        string="Groups",
        comodel_name="res.groups",
        rel="rel_picking_type_print_policy",
        col1="print_id",
        col2="group_id",
    )
    draft_ok = fields.Boolean(
        string="On Draft",
    )
    cancel_ok = fields.Boolean(
        string="On Cancelled",
    )
    waiting_ok = fields.Boolean(
        string="On Waiting Another Operation",
    )
    confirmed_ok = fields.Boolean(
        string="On Waiting Availability",
    )
    partially_available_ok = fields.Boolean(
        string="On Partially Available",
    )
    assigned_ok = fields.Boolean(
        string="On Ready To Transfer",
    )
    done_ok = fields.Boolean(
        string="On Transferred",
    )

    @api.multi
    def action_reload_view(self):
        self.ensure_one()
        if not self.view_id:
            self._create_view()
        else:
            self.view_id.write(self._prepare_view())
        self.view_id.write({"groups_id": self._prepare_group()})

    @api.multi
    def _create_view(self):
        self.ensure_one()
        obj_view = self.env["ir.ui.view"]
        view = obj_view.create(self._prepare_view())
        self.write({"view_id": view.id})

    @api.multi
    def _prepare_view(self):
        self.ensure_one()
        view_name = self.report_id.name
        arch = """<data>
    <xpath expr=\"//field[@name='state']\" position=\"before\">
        <button name=\"%s\" type=\"action\"
            %s string=\"%s\"/>
    </xpath>
</data> """ % (str(self.report_id.id), self._prepare_state() or "", self.name)

        res = {
            "name": view_name,
            "model": "stock.picking",
            "priority": self.original_view_id.priority + 1,
            "type": "form",
            "inherit_id": self.original_view_id.id,
            "mode": "extension",
            "arch": arch,
        }
        return res

    @api.multi
    def _prepare_state(self):
        self.ensure_one()
        res = ""
        if self.draft_ok:
            res += "draft"
        if self.cancel_ok:
            if len(res) > 0:
                res += ","
            res += "cancel"
        if self.waiting_ok:
            if len(res) > 0:
                res += ","
            res += "waiting"
        if self.confirmed_ok:
            if len(res) > 0:
                res += ","
            res += "confirmed"
        if self.partially_available_ok:
            if len(res) > 0:
                res += ","
            res += "partially_available"
        if self.assigned_ok:
            if len(res) > 0:
                res += ","
            res += "assigned"
        if self.done_ok:
            if len(res) > 0:
                res += ","
            res += "done"
        if len(res) > 0:
            return "states=\"%s\"" % (res)
        else:
            return False

    @api.multi
    def _prepare_group(self):
        self.ensure_one()
        if not self.group_ids.ids:
            res = [(6, 0, self.group_ids.ids)]
        else:
            res = [(6, 0, self.group_ids.ids)]
        return res


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    print_policy_ids = fields.One2many(
        string="Print Policy",
        comodel_name="stock.picking_type_print_policy",
        inverse_name="type_id",
    )
