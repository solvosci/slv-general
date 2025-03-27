# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields,_


class SalePurchaseOrderLineMixin(models.AbstractModel):
    _name = 'sale.purchase.order.line.mixin'
    _description = 'Sale and Purchase Order Line Mixin'
    
    sale_purchase_count = fields.Integer(compute='_compute_sale_purchase_count')

    def _get_action_view_domain(self):
        return []
    
    def _get_action_view_context(self):
        return {}
    
    def _compute_sale_purchase_count(self):
        for record in self:
            record.sale_purchase_count = self.env['sale.purchase.order.line'].search_count(
                self._get_action_view_domain()
            )

    def action_sale_purchase_order_line(self):
        return {
            "name": (_("Sale and Purchase Order Lines")),
            "type": "ir.actions.act_window",
            "view_mode": "tree",
            "res_model": "sale.purchase.order.line",
            "domain": self._get_action_view_domain(),
            "context": self._get_action_view_context()
        }
