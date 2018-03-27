# -*- coding: utf-8 -*-
# Copyright 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Stock Picking Wave Type",
    "version": "8.0.1.1.0",
    "summary": "Adds Stock Picking Wave Type",
    "category": "Stock Management",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "stock_picking_wave",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/stock_picking_wave_type_view.xml",
        "views/stock_picking_wave_view.xml",
    ],
}
