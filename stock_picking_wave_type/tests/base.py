# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class BaseStockPickingWaveType(TransactionCase):

    def setUp(self, *args, **kwargs):
        super(BaseStockPickingWaveType, self).setUp(*args, **kwargs)
        # Objects
        self.obj_picking = self.env['stock.picking']
        self.obj_picking_wave = self.env['stock.picking.wave']
        self.obj_picking_wave_type = self.env['stock.picking_wave_type']
        self.obj_ir_sequence = self.env['ir.sequence']
        self.obj_ir_sequence_type = self.env['ir.sequence.type']

        # Data Picking Type
        self.picking_type_1 = self.env.ref(
            'stock.picking_type_in')
        self.picking_type_2 = self.env.ref(
            'stock.picking_type_out')
        self.picking_type_3 = self.env.ref(
            'stock.picking_type_internal')

        # Data Partner
        self.partner = self.env.ref(
            'base.res_partner_1')

        # Data Sequence
        self.sequence = self.env.ref(
            'stock_picking_wave.seq_picking_wave')
        self.new_sequence = self.create_sequence()
        self.type_with_sequence =\
            self.create_type_with_sequence()
        self.type_no_sequence =\
            self.create_type_no_sequence()

    def _get_next_code(self, sequence):
        d = self.obj_ir_sequence._interpolation_dict()
        prefix = self.obj_ir_sequence._interpolate(
            sequence.prefix, d)
        suffix = self.obj_ir_sequence._interpolate(
            sequence.suffix, d)
        code = (prefix + ('%%0%sd' % sequence.padding %
                          sequence.number_next_actual) + suffix)
        return code

    def create_picking_wave(self, type_id):
        picking_wave = self.obj_picking_wave.create({
            'type_id': type_id.id,
            'state': 'in_progress'
        })
        return picking_wave

    def create_sequence(self):
        val_type = {
            'name': 'Picking Wave Type Sequence',
            'code': 'picking.wave.type',
        }
        self.obj_ir_sequence_type.create(val_type)

        val = {
            'name': 'Picking Wave Type Sequence',
            'code': 'picking.wave.type',
            'prefix': 'WVTY',
            'padding': 5
        }
        sequence_id = self.obj_ir_sequence.create(val)

        return sequence_id

    def create_type_with_sequence(self):
        allowed_picking_type_ids = [
            self.picking_type_1.id,
            self.picking_type_2.id
        ]
        val = {
            'name': 'Picking Wave Type 1',
            'sequence_id': self.new_sequence.id,
            'allowed_picking_type_ids': [(6, 0, allowed_picking_type_ids)]
        }
        wave_type_id = self.obj_picking_wave_type.create(val)

        return wave_type_id

    def create_type_no_sequence(self):
        val = {
            'name': 'Picking Wave Type 2'
        }
        wave_type_id = self.obj_picking_wave_type.create(val)

        return wave_type_id
