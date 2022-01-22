# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Picking Selection Policy on Picking Wave",
    "version": "8.0.1.0.0",
    "summary": "Policy for picking selection on picking wave",
    "category": "Stock Management",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "stock_picking_wave_picking_selection",
        "stock_picking_wave_interval",
        "stock_picking_wave_type",
    ],
    "data": [
        "views/stock_picking_wave_type_view.xml",
    ],
}
