# -*- coding: utf-8 -*-
# © 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from .base import TestBasePickingPrintPolicy


class TestReloadView(TestBasePickingPrintPolicy):
    def test_reload_view(self):
        # Create Menu
        self.create_menu(True)

        policy = self.create_policy()
        policy.group_ids = [(
            6, 0, [self.grp_print_picking.id]
        )]
        policy.draft_ok = True
        policy.cancel_ok = True
        policy.waiting_ok = True
        policy.confirmed_ok = True
        policy.partially_available_ok = True
        policy.assigned_ok = True
        policy.done_ok = True
        policy.action_reload_view()

        self.assertIsNotNone(policy.view_id)
