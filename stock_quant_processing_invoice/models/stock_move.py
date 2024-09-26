# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class StockMove(models.Model):
    _inherit = "stock.move"
    _name = "stock.move"

    processing_invoice_ids = fields.One2many(
        string="Processing Invoice",
        comodel_name="stock.move_processing_invoice",
        inverse_name="move_id",
    )

    @api.multi
    def _create_processing_invoice_item(self):
        self.ensure_one()

        obj_processing = self.env["stock.move_processing_invoice"]
        for quant in self.quant_ids.filtered(lambda r: r.owner_id):
            for item in self.picking_type_id.processing_item_ids:
                obj_processing.create(
                    quant._prepare_processing_item(item=item, move=self)
                )
