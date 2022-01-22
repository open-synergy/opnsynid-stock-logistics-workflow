# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Create Fulfillment Service Invoice From Stock Picking, "
    "Stock Move, or Stock Quant",
    "version": "8.0.1.0.0",
    "category": "Stock Management",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "stock_account",
        "base_sequence_configurator",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "data/base_sequence_configurator_data.xml",
        "wizards/create_fulfillment_invoice.xml",
        "views/stock_move_views.xml",
        "views/stock_fulfillment_item_views.xml",
        "views/stock_picking_type_views.xml",
        "views/stock_fulfillment_service_views.xml",
    ],
}
