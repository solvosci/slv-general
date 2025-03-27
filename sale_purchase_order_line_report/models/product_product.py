# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class ProductProduct(models.Model):
    _name = "product.product"
    _inherit = ["product.product", "sale.purchase.order.line.mixin"]

    def _get_action_view_domain(self):
        return [('product_id', '=', self.id)]
    
    def _get_action_view_context(self):
        ret = super()._get_action_view_context()
        ret.update({'hide_sale_purchase_product': True})
        return ret
