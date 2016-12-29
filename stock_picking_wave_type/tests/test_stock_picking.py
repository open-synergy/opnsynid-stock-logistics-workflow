# -*- coding: utf-8 -*-
# Copyright 2016 Michael Viriyananda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from .base import BaseStockPickingWaveType
from openerp.exceptions import Warning as UserError


class TestStockPicking(BaseStockPickingWaveType):
    def test_constrains(self):
        self.picking_wave_3 = self.create_picking_wave(
            self.type_no_sequence)
        new = self.obj_picking.new()
        new.partner_id = self.partner.id
        new.picking_type_id = self.picking_type_3.id
        new.wave_id = self.picking_wave_3.id

        # Check Constrains
        self.assertRaises(
            UserError,
            lambda: new._check_picking_type_id()
        )
