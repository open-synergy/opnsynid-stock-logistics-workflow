# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api


class StockQuant(models.Model):
    _inherit = "stock.quant"
    _name = "stock.quant"

    @api.multi
    def _prepare_processing_item(self, item, move):
        self.ensure_one()
        qty = item.item_id._get_quantity(move=move, quant=self)
        uom_id = item.item_id._get_uom_id(move=move, quant=self)
        pricelist = self._get_processing_pricelist(item=item, move=move)
        currency = pricelist.currency_id
        price = pricelist.price_get(
            prod_id=item.item_id.product_id.id,
            qty=qty
        )[pricelist.id]
        return {
            "quant_id": self.id,
            "partner_id": self.owner_id.id,
            "item_id": item.item_id.id,
            "move_id": move.id,
            "price_unit": price,
            "currency_id": currency.id,
            "quantity": qty,
            "uom_id": uom_id,
            "tax_ids": [
                (6, 0, item.item_id.product_id.taxes_id.ids),
            ],
        }

    @api.multi
    def _get_processing_pricelist(self, item, move):
        if item.pricelist_id:
            return item.pricelist_id
