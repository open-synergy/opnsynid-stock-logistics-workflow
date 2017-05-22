# -*- coding: utf-8 -*-
# © 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from .base import TestBasePickingPrintPolicy


class TestComputeNoWindowAction(TestBasePickingPrintPolicy):
    def test_compute_no_window_action(self):
        # Check Menu
        self.assertEqual(
            False,
            self.picking_type.menu_id.id
        )

        # Check Window Action
        self.assertEqual(
            False,
            self.picking_type.window_action_id.id
        )

        policy = self.create_policy()

        self.assertEqual(False, policy.original_view_id.id)
