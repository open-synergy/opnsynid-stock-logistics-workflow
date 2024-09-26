# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api


class ProductProduct(models.Model):
    _inherit = "product.product"
    _name = "product.product"

    @api.multi
    def _get_processing_account_id(self):
        self.ensure_one()
        if self.categ_id.property_account_income_categ:
            return self.categ_id.property_account_income_categ.id

        if self.property_account_income:
            return self.property_account_income.id

        return False
