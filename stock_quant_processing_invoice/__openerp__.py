# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Create Invoice For Stock Move Processing",
    "version": "8.0.1.0.0",
    "category": "Stock Management",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "stock_picking_package_info",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizards/create_processing_invoice.xml",
        "views/stock_move_views.xml",
        "views/stock_move_processing_item_views.xml",
        "views/stock_picking_type_views.xml",
        "views/stock_move_processing_invoice_views.xml",
    ],
}
