# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Stock Picking Cancellation Reason",
    "version": "8.0.1.0.0",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "category": "Stock Management",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "stock",
    ],
    "data": [
        "wizards/stock_picking_cancel.xml",
        "views/stock_picking_cancel_reason_view.xml",
        "views/stock_picking_view.xml",
        "security/ir.model.access.csv"
    ],
}
