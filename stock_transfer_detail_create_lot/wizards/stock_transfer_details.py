# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models


class StockTransferDetails(models.TransientModel):
    _inherit = "stock.transfer_details"

    @api.multi
    def button_generate_lot(self):
        self.ensure_one()
        for detail in self.item_ids:
            detail.with_context({"date_sequence": detail.date})._generate_lot()
        return self.wizard_view()


class StockTransferDetailsItems(models.TransientModel):
    _inherit = "stock.transfer_details_items"

    @api.multi
    def _generate_lot(self):
        self.ensure_one()
        obj_lot = self.env["stock.production.lot"]
        lot = obj_lot.create(self._prepare_generate_lot())
        self.write({"lot_id": lot.id})

    @api.multi
    def _prepare_generate_lot(self):
        return {
            "name": "/",
            "product_id": self.product_id.id,
        }
