# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Stock Picking Manual Invoice Link",
    "version": "8.0.1.0.0",
    "category": "Stock Management",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "stock_picking_invoice_link",
    ],
    "data": [
        "wizards/stock_picking_manual_invoice_link.xml",
        "views/stock_picking_views.xml",
    ],
}
