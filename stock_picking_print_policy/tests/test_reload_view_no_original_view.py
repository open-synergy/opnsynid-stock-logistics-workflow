# -*- coding: utf-8 -*-
# © 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from .base import TestBasePickingPrintPolicy
from openerp.exceptions import Warning as UserError


class TestReloadViewNoOriginalView(TestBasePickingPrintPolicy):
    def test_compute_no_view(self):
        # Create Menu
        self.create_menu()

        policy = self.create_policy()

        # Check UserError
        msg = "No Original View"
        with self.assertRaises(UserError) as error:
            policy.action_reload_view()
        self.assertEqual(error.exception.message, msg)
