# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestBasePickingPrintPolicy(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestBasePickingPrintPolicy, self).setUp(*args, **kwargs)
        # Object
        self.wiz =\
            self.env["stock.operation_type_create_menu"]
        self.obj_picking_type =\
            self.env["stock.picking.type"]
        self.obj_print_policy =\
            self.env["stock.picking_type_print_policy"]
        self.obj_act_window_view =\
            self.env['ir.actions.act_window.view']
        self.wiz_view =\
            self.env["stock.operation_type_create_menu_view_detail"]
        self.obj_res_groups = self.env['res.groups']

        # Data
        self.picking_type =\
            self.env.ref("stock.picking_type_in")
        self.report_id =\
            self.env.ref("stock.action_report_picking")
        self.tree_view =\
            self.env.ref("stock.vpicktree")
        self.form_view =\
            self.env.ref("stock.view_picking_form")

        # Add Group
        self.grp_print_picking = self.obj_res_groups.create({
            'name': 'Group Print Picking'
        })

    def create_menu(self, view=False):
        new = self.wiz.with_context(
            active_model="stock.picking.type",
            active_ids=[self.picking_type.id]
        ).new()
        new.menu_name = self.picking_type.name
        if view:
            new.view_ids = [
                (0, 0, {
                    "sequence": 1,
                    "view_id": self.tree_view.id,
                    "view_mode": "tree"}),
                (0, 0, {
                    "sequence": 2,
                    "view_id": self.form_view.id,
                    "view_mode": "form"})
            ]
        new.button_create_menu()

    def create_policy(self):
        vals = {
            "type_id": self.picking_type.id,
            "name": "Test - Button Print",
            "report_id": self.report_id.id
        }

        policy = self.obj_print_policy.create(vals)

        return policy
