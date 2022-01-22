# -*- coding: utf-8 -*-
# Copyright 2021 PT. Simetri Sinergi Indonesia
# Copyright 2021 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class StockInventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    theoretical_qty_method = fields.Selection(
        string="Theoretical Qty Method",
        selection=[
            ("automatic", "Automatic"),
            ("manual", "Manual"),
        ],
        required=True,
        default="automatic",
    )
    manual_theoretical_qty = fields.Float(
        string="Manual Theoretical Qty",
    )

    @api.multi
    @api.depends(
        "theoretical_qty_method",
        "manual_theoretical_qty",
        "location_id",
        "product_id",
        "package_id",
        "product_uom_id",
        "company_id",
        "prod_lot_id",
        "partner_id",
    )
    def _compute_theoretical_qty_new(self):
        obj_stock_quant = self.env["stock.quant"]
        obj_product_uom = self.env["product.uom"]
        for document in self:
            if document.theoretical_qty_method == "automatic":
                quant_ids = self._get_quants(document)
                quants = obj_stock_quant.browse(quant_ids)
                tot_qty = sum(x.qty for x in quants)
                product_uom_id = document.product_uom_id
                uom_id = document.product_id.uom_id.id
                if product_uom_id and uom_id != document.product_uom_id.id:
                    tot_qty = obj_product_uom._compute_qty_obj(
                        document.product_id.uom_id, tot_qty, document.product_uom_id
                    )
                document.theoretical_qty = tot_qty
            else:
                document.theoretical_qty = document.manual_theoretical_qty

    theoretical_qty = fields.Float(
        compute="_compute_theoretical_qty_new",
    )
