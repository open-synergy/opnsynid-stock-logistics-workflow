# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from lxml import etree
from openerp import api, fields, models


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    location_id = fields.Many2one(
        default=lambda self: False,
    )

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        res = super(StockInventory, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu
        )
        doc = etree.XML(res["arch"])
        domain = []
        list_location_ids = []
        obj_stock_location = self.env["stock.location"]
        location_ids = obj_stock_location.search([])
        for location in location_ids:
            if self.env.user.id in location.all_user_inventory_ids.ids:
                list_location_ids.append(location.id)
        if list_location_ids:
            domain = [("id", "in", list_location_ids)]
        if domain:
            for node in doc.xpath("//field[@name='location_id']"):
                node.set("domain", str(domain))
        res["arch"] = etree.tostring(doc)
        return res
