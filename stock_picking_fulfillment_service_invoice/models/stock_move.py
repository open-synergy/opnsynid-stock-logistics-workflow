# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"
    _name = "stock.move"

    fulfillment_service_ids = fields.One2many(
        string="Fulfillment Services",
        comodel_name="stock.fulfillment_service",
        inverse_name="move_id",
    )

    @api.multi
    def _create_fulfillment_service(self):
        self.ensure_one()
        if not self.restrict_partner_id:
            return True

        obj_service = self.env["stock.fulfillment_service"]
        ptype = self.picking_type_id
        for item in ptype.fulfillment_item_ids.filtered(
            lambda r: r.item_id.applicable_on == "move"
        ):
            obj_service.create(self._prepare_fulfillment_service(item=item))

    @api.multi
    def _get_processing_pricelist(self, item):
        if item.pricelist_id:
            return item.pricelist_id

    @api.multi
    def _prepare_fulfillment_service(self, item):
        self.ensure_one()
        qty = item.item_id._get_quantity(document=self)
        uom_id = item.item_id._get_uom_id(document=self)
        pricelist = self._get_processing_pricelist(item=item)
        currency = pricelist.currency_id
        price = pricelist.price_get(prod_id=item.item_id.product_id.id, qty=qty)[
            pricelist.id
        ]
        return {
            "move_id": self.id,
            "partner_id": self.restrict_partner_id.id,
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
    def action_done(self):
        _super = super(StockMove, self)
        _super.action_done()
        for move in self:
            move._create_fulfillment_service()
            for quant in move.quant_ids:
                quant._create_fulfillment_service(move)
