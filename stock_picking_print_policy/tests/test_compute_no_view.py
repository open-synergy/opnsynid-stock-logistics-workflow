# -*- coding: utf-8 -*-
# © 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from .base import TestBasePickingPrintPolicy


class TestComputeNoView(TestBasePickingPrintPolicy):
    def test_compute_no_view(self):
        # Create Menu
        self.create_menu()

        view_id = self.obj_act_window_view.search(
            [('act_window_id', '=', self.picking_type.window_action_id.id)]
        )

        # Check View
        self.assertEqual(
            False,
            view_id.id
        )

        policy = self.create_policy()

        self.assertEqual(
            False,
            policy.original_view_id.id
        )
