# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields


class StockQuant(models.Model):
    _inherit = "stock.quant"
    _name = "stock.quant"

    fulfillment_service_ids = fields.One2many(
        string="Fulfillment Services",
        comodel_name="stock.fulfillment_service",
        inverse_name="quant_id",
    )

    @api.multi
    def _create_fulfillment_service(self, move):
        self.ensure_one()
        if not self.owner_id:
            return True

        obj_service = self.env["stock.fulfillment_service"]
        ptype = move.picking_type_id
        for item in ptype.fulfillment_item_ids.filtered(
                lambda r: r.item_id.applicable_on == "quant"):
            obj_service.create(
                self._prepare_fulfillment_service(item=item, move=move)
            )

    @api.multi
    def _get_processing_pricelist(self, item):
        if item.pricelist_id:
            return item.pricelist_id

    @api.multi
    def _prepare_fulfillment_service(self, item, move):
        self.ensure_one()
        qty = item.item_id._get_quantity(document=self)
        uom_id = item.item_id._get_uom_id(document=self)
        pricelist = self._get_processing_pricelist(item=item)
        currency = pricelist.currency_id
        price = pricelist.price_get(
            prod_id=item.item_id.product_id.id,
            qty=qty
        )[pricelist.id]
        return {
            "quant_id": self.id,
            "partner_id": self.owner_id.id,
            "item_id": item.item_id.id,
            "price_unit": price,
            "currency_id": currency.id,
            "quantity": qty,
            "uom_id": uom_id,
            "tax_ids": [
                (6, 0, item.item_id.product_id.taxes_id.ids),
            ],
        }

    @api.multi
    def _get_processing_pricelist(self, item):
        if item.pricelist_id:
            return item.pricelist_id
