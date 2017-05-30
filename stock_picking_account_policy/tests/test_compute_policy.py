# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase


class TestComputePickingAccountPolicy(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestComputePickingAccountPolicy, self).setUp(*args, **kwargs)
        # Objects
        self.obj_stock_picking = self.env['stock.picking']
        self.obj_res_groups = self.env['res.groups']
        self.obj_res_users = self.env['res.users']

        # Data
        self.supplier_location =\
            self.env.ref('stock.stock_location_suppliers')
        self.stock_location =\
            self.env.ref('stock.stock_location_stock')
        self.product =\
            self.env.ref('product.product_product_8')
        self.picking_type_out =\
            self.env.ref("stock.picking_type_out")
        self.group_employee_id = self.ref('base.group_user')
        self.grp_stock_manager =\
            self.env.ref('stock.group_stock_manager')
        self.user = self._create_user()

        # Add Group Button Invoice
        self.grp_invoice = self.obj_res_groups.create({
            'name': 'Group Button Invoice'
        })

    def _create_user(self):
        val = {
            'name': 'User Test',
            'login': 'user',
            'alias_name': 'user',
            'email': 'user_test@example.com',
            'notify_email': 'none',
            'groups_id': [(
                6, 0, [
                    self.group_employee_id,
                    self.grp_stock_manager.id
                ]
            )]
        }
        user = self.obj_res_users.with_context({
            'no_reset_password': True
        }).create(val)
        return user

    def _create_stock_picking(self, picking_type):
        if picking_type:
            type_id = picking_type.id
        else:
            type_id = False

        # Create Stock Picking
        picking = self.obj_stock_picking.create({
            'picking_type_id': type_id,
            'move_lines': [(0, 0, {
                'name': self.product.name,
                'product_id': self.product.id,
                'product_uom': self.product.uom_id.id,
                'location_id': self.supplier_location.id,
                'location_dest_id': self.stock_location.id
            })]
        })

        return picking

    def test_compute_case_admin(self):
        # Create Stock Picking
        picking =\
            self._create_stock_picking(self.picking_type_out)

        # Condition :
        #   1. Test for User Admin
        self.assertEqual(True, picking.invoice_ok)

    def test_compute_case_1(self):
        # Create Stock Picking
        picking =\
            self._create_stock_picking(self.picking_type_out)

        # Condition :
        #   1. Log In As User Test
        #   2. Allowed to Invoice has group
        #   4. User doesn't have group
        self.picking_type_out.invoice_group_ids = [(
            6, 0, [
                self.grp_invoice.id
            ]
        )]

        # Result
        #   1. User Test cannot Invoice

        self.assertEqual(
            False,
            picking.sudo(
                self.user.id).invoice_ok
        )

        # Condition :
        #   1. User Test have group
        # Add Group Invoice
        self.user.groups_id = [(
            4,
            self.grp_invoice.id
        )]

        # Result
        #   1. User Test can Invoice
        self.assertEqual(
            True,
            picking.sudo(
                self.user.id).invoice_ok
        )
