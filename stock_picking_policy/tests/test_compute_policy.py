# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase


class TestComputePickingPolicy(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestComputePickingPolicy, self).setUp(*args, **kwargs)
        # Objects
        self.obj_stock_picking = self.env["stock.picking"]
        self.obj_res_groups = self.env["res.groups"]
        self.obj_res_users = self.env["res.users"]

        # Data
        self.supplier_location = self.env.ref("stock.stock_location_suppliers")
        self.stock_location = self.env.ref("stock.stock_location_stock")
        self.product = self.env.ref("product.product_product_8")
        self.picking_type_out = self.env.ref("stock.picking_type_out")
        self.group_employee_id = self.ref("base.group_user")
        self.grp_stock_manager = self.env.ref("stock.group_stock_manager")
        self.user_1 = self._create_user_1()
        self.user_2 = self._create_user_2()
        self.user_3 = self._create_user_3()

        # Add Group Button Confirm
        self.grp_confirm = self.obj_res_groups.create(
            {"name": "Group Button Confirm Call"}
        )
        # Add Group Button Force Availability
        self.grp_force = self.obj_res_groups.create(
            {"name": "Group Button Force Availability"}
        )
        # Add Group Button Transfer
        self.grp_transfer = self.obj_res_groups.create(
            {"name": "Group Button Transfer"}
        )
        # Add Group Button Return
        self.grp_return = self.obj_res_groups.create({"name": "Group Button Return"})
        # Add Group Button Done
        self.grp_cancel = self.obj_res_groups.create({"name": "Group Button Cancel"})
        # Add Group Button Unreserve
        self.grp_unreserve = self.obj_res_groups.create(
            {"name": "Group Button Unreserve"}
        )

    def _create_user_1(self):
        val = {
            "name": "User Test 1",
            "login": "user_1",
            "alias_name": "user1",
            "email": "user_test_1@example.com",
            "notify_email": "none",
            "groups_id": [(6, 0, [self.group_employee_id, self.grp_stock_manager.id])],
        }
        user_1 = self.obj_res_users.with_context({"no_reset_password": True}).create(
            val
        )
        return user_1

    def _create_user_2(self):
        val = {
            "name": "User Test 2",
            "login": "user_2",
            "alias_name": "user2",
            "email": "user_test_2@example.com",
            "notify_email": "none",
            "groups_id": [(6, 0, [self.group_employee_id, self.grp_stock_manager.id])],
        }
        user_2 = self.obj_res_users.with_context({"no_reset_password": True}).create(
            val
        )
        return user_2

    def _create_user_3(self):
        val = {
            "name": "User Test 3",
            "login": "user_3",
            "alias_name": "user3",
            "email": "user_test_3@example.com",
            "notify_email": "none",
            "groups_id": [(6, 0, [self.group_employee_id, self.grp_stock_manager.id])],
        }
        user_3 = self.obj_res_users.with_context({"no_reset_password": True}).create(
            val
        )
        return user_3

    def _create_stock_picking(self, picking_type):
        if picking_type:
            type_id = picking_type.id
        else:
            type_id = False

        # Create Stock Picking
        picking = self.obj_stock_picking.create(
            {
                "picking_type_id": type_id,
                "move_lines": [
                    (
                        0,
                        0,
                        {
                            "name": self.product.name,
                            "product_id": self.product.id,
                            "product_uom": self.product.uom_id.id,
                            "location_id": self.supplier_location.id,
                            "location_dest_id": self.stock_location.id,
                        },
                    )
                ],
            }
        )

        return picking

    def test_compute_case_admin(self):
        # Create Stock Picking
        picking = self._create_stock_picking(self.picking_type_out)

        # Condition :
        #   1. Test for User Admin
        self.assertEqual(True, picking.confirm_ok)
        self.assertEqual(True, picking.force_ok)
        self.assertEqual(True, picking.transfer_ok)
        self.assertEqual(True, picking.return_ok)
        self.assertEqual(True, picking.cancel_ok)
        self.assertEqual(True, picking.unreserve_ok)

    def test_compute_case_1(self):
        # Create Stock Picking
        picking = self._create_stock_picking(self.picking_type_out)

        # Condition :
        #   1. Log In As User 1
        #   2. Allowed to Confirm has group
        #   3. Allowed to Force Availability has group
        #   4. User 1 doesn't have group
        self.picking_type_out.confirm_group_ids = [(6, 0, [self.grp_confirm.id])]

        self.picking_type_out.force_group_ids = [(6, 0, [self.grp_force.id])]
        # Result
        #   1. User 1 cannot Confirm
        #   2. User 1 cannot Force Availability

        self.assertEqual(False, picking.sudo(self.user_1.id).confirm_ok)
        self.assertEqual(False, picking.sudo(self.user_1.id).force_ok)
        self.assertEqual(True, picking.sudo(self.user_1.id).transfer_ok)
        self.assertEqual(True, picking.sudo(self.user_1.id).return_ok)
        self.assertEqual(True, picking.sudo(self.user_1.id).cancel_ok)
        self.assertEqual(True, picking.sudo(self.user_1.id).unreserve_ok)

        # Condition :
        #   1. User 1 have group
        # Add Group Confirm
        self.user_1.groups_id = [(4, self.grp_confirm.id)]
        # Add Group Force Availability
        self.user_1.groups_id = [(4, self.grp_force.id)]

        # Result
        #   1. User 1 can Confirm
        #   2. User 1 can Force Availability
        self.assertEqual(True, picking.sudo(self.user_1.id).confirm_ok)
        self.assertEqual(True, picking.sudo(self.user_1.id).force_ok)
        self.assertEqual(True, picking.sudo(self.user_1.id).transfer_ok)
        self.assertEqual(True, picking.sudo(self.user_1.id).return_ok)
        self.assertEqual(True, picking.sudo(self.user_1.id).cancel_ok)
        self.assertEqual(True, picking.sudo(self.user_1.id).unreserve_ok)

    def test_compute_case_2(self):
        # Create Stock Picking
        picking = self._create_stock_picking(self.picking_type_out)

        # Condition :
        #   1. Log In As User 2
        #   2. Allowed to Transfer has group
        #   3. Allowed to Return has group
        #   4. User 2 doesn't have group
        self.picking_type_out.transfer_group_ids = [(6, 0, [self.grp_transfer.id])]

        self.picking_type_out.return_group_ids = [(6, 0, [self.grp_return.id])]
        # Result
        #   1. User 2 cannot Transfer
        #   2. User 2 cannot Return

        self.assertEqual(True, picking.sudo(self.user_2.id).confirm_ok)
        self.assertEqual(True, picking.sudo(self.user_2.id).force_ok)
        self.assertEqual(False, picking.sudo(self.user_2.id).transfer_ok)
        self.assertEqual(False, picking.sudo(self.user_2.id).return_ok)
        self.assertEqual(True, picking.sudo(self.user_2.id).cancel_ok)
        self.assertEqual(True, picking.sudo(self.user_2.id).unreserve_ok)

        # Condition :
        #   1. User 2 have group
        # Add Group Transfer
        self.user_2.groups_id = [(4, self.grp_transfer.id)]
        # Add Group Return
        self.user_2.groups_id = [(4, self.grp_return.id)]

        # Result
        #   1. User 2 can Transfer
        #   2. User 2 can Return
        self.assertEqual(True, picking.sudo(self.user_2.id).confirm_ok)
        self.assertEqual(True, picking.sudo(self.user_2.id).force_ok)
        self.assertEqual(True, picking.sudo(self.user_2.id).transfer_ok)
        self.assertEqual(True, picking.sudo(self.user_2.id).return_ok)
        self.assertEqual(True, picking.sudo(self.user_2.id).cancel_ok)
        self.assertEqual(True, picking.sudo(self.user_2.id).unreserve_ok)

    def test_compute_case_3(self):
        # Create Stock Picking
        picking = self._create_stock_picking(self.picking_type_out)

        # Condition :
        #   1. Log In As User 3
        #   2. Allowed to Cancel has group
        #   3. Allowed to Unreserve has group
        #   4. User 3 doesn't have group
        self.picking_type_out.cancel_group_ids = [(6, 0, [self.grp_cancel.id])]

        self.picking_type_out.unreserve_group_ids = [(6, 0, [self.grp_unreserve.id])]
        # Result
        #   1. User 3 cannot Cancel
        #   2. User 3 cannot Unreserve

        self.assertEqual(True, picking.sudo(self.user_3.id).confirm_ok)
        self.assertEqual(True, picking.sudo(self.user_3.id).force_ok)
        self.assertEqual(True, picking.sudo(self.user_3.id).transfer_ok)
        self.assertEqual(True, picking.sudo(self.user_3.id).return_ok)
        self.assertEqual(False, picking.sudo(self.user_3.id).cancel_ok)
        self.assertEqual(False, picking.sudo(self.user_3.id).unreserve_ok)

        # Condition :
        #   1. User 3 have group
        # Add Group Cancel
        self.user_3.groups_id = [(4, self.grp_cancel.id)]
        # Add Group Unreserve
        self.user_3.groups_id = [(4, self.grp_unreserve.id)]

        # Result
        #   1. User 3 can Cancel
        #   2. User 3 can Unreserve
        self.assertEqual(True, picking.sudo(self.user_3.id).confirm_ok)
        self.assertEqual(True, picking.sudo(self.user_3.id).force_ok)
        self.assertEqual(True, picking.sudo(self.user_3.id).transfer_ok)
        self.assertEqual(True, picking.sudo(self.user_3.id).return_ok)
        self.assertEqual(True, picking.sudo(self.user_3.id).cancel_ok)
        self.assertEqual(True, picking.sudo(self.user_3.id).unreserve_ok)
