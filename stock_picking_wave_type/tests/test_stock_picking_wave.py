# -*- coding: utf-8 -*-
# Copyright 2016 Michael Viriyananda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from .base import BaseStockPickingWaveType


class TestStockPickingWave(BaseStockPickingWaveType):

    def test_create_with_sequence(self):
        sequence_id =\
            self.type_with_sequence.sequence_id
        code = self._get_next_code(sequence_id)

        self.picking_wave_1 = self.create_picking_wave(
            self.type_with_sequence)

        self.assertNotEqual(self.picking_wave_1.name, '/')
        self.assertEqual(self.picking_wave_1.name, code)

    def test_create_no_sequence(self):
        sequence_id = self.sequence
        code = self._get_next_code(sequence_id)

        self.picking_wave_2 = self.create_picking_wave(
            self.type_no_sequence)

        self.assertNotEqual(self.picking_wave_2.name, '/')
        self.assertEqual(self.picking_wave_2.name, code)
