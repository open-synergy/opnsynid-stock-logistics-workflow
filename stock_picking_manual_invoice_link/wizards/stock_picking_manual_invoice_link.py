# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class StockPickingManualInvoiceLink(models.TransientModel):
    _name = "stock.picking_manual_invoice_link"
    _description = "Link Picking to Invoice Manually"

    @api.model
    def _default_picking_id(self):
        return self._context.get("active_id", False)

    picking_id = fields.Many2one(
        string="Picking",
        comodel_name="stock.picking",
        default=lambda self: self._default_picking_id(),
    )
    invoice_id = fields.Many2one(
        string="Invoice",
        comodel_name="account.invoice",
    )
    line_ids = fields.One2many(
        string="Detail",
        comodel_name="stock.picking_manual_invoice_link_line",
        inverse_name="wizard_id",
    )

    @api.multi
    def onchange_picking_id(self, picking_id):
        value = self._get_value_before_onchange_picking_id()
        domain = self._get_domain_before_onchange_picking_id()
        if picking_id:
            obj_picking = self.env["stock.picking"]
            picking = obj_picking.browse([picking_id])[0]
            value = self._get_value_after_onchange_picking_id(picking)
            domain = self._get_domain_after_onchange_picking_id(picking)
        return {"value": value, "domain": domain}

    @api.multi
    def _get_value_before_onchange_picking_id(self):
        return {
            "invoice_id": False,
            "line_ids": [],
        }

    @api.multi
    def _get_domain_before_onchange_picking_id(self):
        return {}

    @api.multi
    def _get_value_after_onchange_picking_id(self, picking):
        result = {
            "line_ids": self._get_stock_move_lines(picking),
        }
        return result

    @api.model
    def _get_stock_move_lines(self, picking):
        result = []
        for line in picking.move_lines:
            result.append(
                (
                    0,
                    0,
                    {
                        "stock_move_id": line.id,
                    },
                )
            )
        return result

    @api.multi
    def _get_domain_after_onchange_picking_id(self, picking):
        partner = picking.partner_id
        result = {
            "invoice_id": [
                ("id", "=", 0),
            ]
        }
        inv_type = self._map_picking_type_2_invoice_type(picking)
        if partner:
            result.update(
                {
                    "invoice_id": [
                        ("partner_id.commercial_partner_id.id", "=", partner.id),
                        ("state", "in", ["open", "paid"]),
                        ("picking_ids", "=", False),
                        ("type", "in", inv_type),
                    ]
                }
            )
        return result

    @api.model
    def _map_picking_type_2_invoice_type(self, picking):
        result = []
        ptype = picking.picking_type_id
        if ptype.code == "outgoing":
            result = ["out_invoice", "in_refund"]
        elif ptype.code == "incoming":
            result = ["in_invoice", "out_refund"]
        return result

    @api.multi
    def button_confirm(self):
        self.ensure_one()
        picking = self.picking_id
        picking.write(self._prepare_picking_data())
        for line in self.line_ids:
            line.stock_move_id.write(line._prepare_stock_move_data())

    @api.multi
    def _prepare_picking_data(self):
        self.ensure_one()
        return {
            "invoice_ids": [(6, 0, [self.invoice_id.id])],
            "invoice_state": "invoiced",
        }

    @api.multi
    def _prepare_invoice_data(self):
        self.ensure_one()
        return {
            "picking_ids": [(6, 0, [self.picking_id.id])],
        }


class StockPickingManualInvoiceLinkLine(models.TransientModel):
    _name = "stock.picking_manual_invoice_link_line"
    _description = "Link Picking to Invoice Manually Line"

    @api.multi
    @api.depends("stock_move_id")
    def _compute_stock_move(self):
        for line in self:
            move = line.stock_move_id
            line.product_id = move.product_id.id
            line.picking_qty = move.product_uom_qty

    wizard_id = fields.Many2one(
        string="Wizard",
        comodel_name="stock.picking_manual_invoice_link",
    )
    invoice_id = fields.Many2one(
        string="Invoice",
        comodel_name="account.invoice",
        related="wizard_id.invoice_id",
        store=False,
    )
    invoice_line_id = fields.Many2one(
        string="Invoice Line",
        comodel_name="account.invoice.line",
    )
    stock_move_id = fields.Many2one(
        string="Stock Move",
        comodel_name="stock.move",
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        compute="_compute_stock_move",
        related=False,
        store=False,
    )
    invoice_qty = fields.Float(
        string="Invoice Qty.",
        compute="_compute_stock_move",
        related=False,
        store=False,
    )
    picking_qty = fields.Float(
        string="Picking Qty.",
        related="stock_move_id.product_uom_qty",
    )

    @api.onchange("invoice_id")
    def onchange_invoice_id(self):
        self.invoice_line_id = False

    @api.multi
    def _prepare_stock_move_data(self):
        self.ensure_one()
        result = {"invoice_line_ids": [(6, 0, [self.invoice_line_id.id])]}
        return result

    @api.multi
    def _prepare_invoice_line_data(self):
        self.ensure_one()
        result = {"move_line_ids": [(6, 0, [self.stock_move_id.id])]}
        return result
