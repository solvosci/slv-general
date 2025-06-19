# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = ["product.template", "sale.purchase.order.line.mixin"]

    def _get_action_view_domain(self):
        return [('product_id', 'in', self.product_variant_ids.ids)]

    def _get_action_view_context(self):
        ret = super()._get_action_view_context()
        ret.update({'hide_sale_purchase_product': True})
        return ret
