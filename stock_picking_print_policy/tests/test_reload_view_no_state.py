# -*- coding: utf-8 -*-
# © 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from .base import TestBasePickingPrintPolicy


class TestReloadViewNoState(TestBasePickingPrintPolicy):
    def test_reload_no_state(self):
        # Create Menu
        self.create_menu(True)

        policy = self.create_policy()
        policy.action_reload_view()

        self.assertIsNotNone(policy.view_id)
