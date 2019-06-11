# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade
from openerp import api, SUPERUSER_ID


@openupgrade.migrate()
def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    if openupgrade.table_exists(env.cr, "stock_picking_type_print_policy"):
        openupgrade.logged_query(
            cr,
            """
            DROP TABLE stock_picking_type_print_policy CASCADE
            """)
