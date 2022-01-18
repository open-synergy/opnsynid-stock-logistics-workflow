# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Stock Location Rent",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "installable": True,
    "application": True,
    "depends": [
        "stock",
        "base_sequence_configurator",
        "base_workflow_policy",
        "base_cancel_reason",
        "base_terminate_reason",
        "base_multiple_approval",
        "base_print_policy",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "data/base_sequence_configurator_data.xml",
        "data/base_cancel_reason_configurator_data.xml",
        "data/base_terminate_reason_configurator_data.xml",
        "data/base_workflow_policy_data.xml",
        "menu.xml",
        "views/stock_location_rent_type_views.xml",
        "views/stock_location_rent_payment_term_detail_views.xml",
        "views/stock_location_rent_detail_views.xml",
        "views/stock_location_rent_views.xml",
    ],
    "demo": [],
}
