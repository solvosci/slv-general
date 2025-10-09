# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class SalePurchaseOrderLine(models.Model):
    _inherit = 'sale.purchase.order.line'

    refund_qty = fields.Float('Refunded quantity', readonly=True)
    net_product_uom_qty = fields.Float('Net Quantity', readonly=True)
    net_price_subtotal = fields.Float('Net Subtotal', readonly=True)

    def _select_extra_sale(self):
        return """,
            SUM(pol_ref.qty) AS refund_qty,
            (CASE com.sale_purchase_history_mode
                WHEN 'qty_ordered' THEN sol.product_uom_qty + COALESCE(SUM(pol_ref.qty), 0)
                WHEN 'qty_rec_and_del' THEN sol.qty_delivered + COALESCE(SUM(pol_ref.qty), 0)
            END) AS net_product_uom_qty,
            (CASE com.sale_purchase_history_mode
                WHEN 'qty_ordered' THEN sol.price_subtotal * (sol.product_uom_qty + COALESCE(SUM(pol_ref.qty),0)) / NULLIF(sol.product_uom_qty,0)
                WHEN 'qty_rec_and_del' THEN sol.price_subtotal * (sol.qty_delivered + COALESCE(SUM(pol_ref.qty),0)) / NULLIF(sol.qty_delivered,0)
            END) AS net_price_subtotal"""

    def _from_extra_sale(self):
        return """
            LEFT JOIN pos_order_line pol
                ON pol.sale_order_origin_id = so.id
            LEFT JOIN pos_order_line pol_ref
                ON pol_ref.refunded_orderline_id = pol.id
            """

    def _select_extra_purchase(self):
        return """,
            0 AS refund_qty,
            (CASE com.sale_purchase_history_mode
                WHEN 'qty_ordered' THEN pol.product_uom_qty
                WHEN 'qty_rec_and_del' THEN pol.qty_received
            END) AS net_product_uom_qty,
            (CASE com.sale_purchase_history_mode
                WHEN 'qty_ordered' THEN pol.price_subtotal
                WHEN 'qty_rec_and_del' THEN pol.price_subtotal
            END) AS net_price_subtotal"""
