# Copyright 2015-2016 Agile Business Group (<http://www.agilebg.com>)
# Copyright 2015 BREMSKERL-REIBBELAGWERKE EMMERLING GmbH & Co. KG
#    Author Marco Dieckhoff
# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# pylint: disable=locally-disabled, manifest-required-author
{
    "name": "Stock Move Backdating",
    "version": "12.0.1.0.1",
    "category": "Stock Logistics",
    "author": "Marco Dieckhoff, BREMSKERL, Agile Business Group, "
    "Odoo Community Association (OCA), "
    "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "website": "https://simetri-sinergi.id",
    "depends": [
        "stock_account",
    ],
    "data": [
        "views/stock_picking_view.xml",
    ],
    "installable": True,
}
