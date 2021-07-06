# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Auto Create Serial Number From Transfer Detail",
    "version": "8.0.2.0.0",
    "category": "Stock Management",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "stock_production_lot_by_product",
        "stock_move_backdating",
    ],
    "data": [
        "wizards/stock_transfer_details.xml",
    ],
}
