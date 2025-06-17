# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, tools, _


class SalePurchaseOrderLine(models.Model):
    _name = 'sale.purchase.order.line'
    _description = 'Combined Sale and Purchase Order Lines'
    _auto = False 

    date_order = fields.Datetime('Order Date', readonly=True)
    order_name = fields.Char('Order', readonly=True, index=True)
    sale_order_id = fields.Many2one('sale.order', readonly=True)
    purchase_order_id = fields.Many2one('purchase.order', readonly=True)
    partner_id = fields.Many2one('res.partner', readonly=True)
    product_id = fields.Many2one('product.product', readonly=True)
    product_uom_qty = fields.Float('Quantity', readonly=True)
    price_unit = fields.Float('Unit Price', readonly=True)
    discount = fields.Float('Discount', readonly=True)
    price_subtotal = fields.Float('Subtotal', readonly=True)
    type = fields.Selection([('sale', 'Sale'), ('purchase', 'Purchase')], 'Type', readonly=True)
    currency_id = fields.Many2one('res.currency', readonly=True)
    company_id = fields.Many2one('res.company', readonly=True)

    sale_purchase_history_mode = fields.Selection([
            ("qty_ordered", "Quantities ordered"),
            ("qty_rec_and_del", "Quantities received and delivered"),
    ], string="Sale/Purchase history mode")

    qty_delivered = fields.Float('Delivery Quantity', readonly=True)
    qty_received = fields.Float('Received Qty', readonly=True)

    def init(self):
        tools.drop_view_if_exists(self._cr, 'sale_purchase_order_line')
        self._cr.execute('''
            CREATE VIEW %s AS 
                (
                    SELECT sol.id * 2 AS id, so.date_order, so.name AS order_name, so.id AS sale_order_id, NULL AS purchase_order_id,
                    sol.order_partner_id AS partner_id, sol.company_id, sol.product_id,
                    com.sale_purchase_history_mode,
                    CASE com.sale_purchase_history_mode
                        WHEN 'qty_ordered' THEN sol.product_uom_qty
                        WHEN 'qty_rec_and_del' THEN sol.qty_delivered
                    END AS product_uom_qty,
                    sol.price_unit,
                    sol.discount,
                    CASE com.sale_purchase_history_mode
                        WHEN 'qty_ordered' THEN sol.price_subtotal
                        WHEN 'qty_rec_and_del' THEN sol.price_subtotal * sol.qty_delivered / NULLIF(sol.product_uom_qty, 0)
                    END AS price_subtotal,
                    so.currency_id, 'sale' AS type, sol.qty_delivered, 0 as qty_received
                    FROM sale_order_line sol
                    INNER JOIN sale_order so ON sol.order_id = so.id
                    INNER JOIN res_company com ON com.id = sol.company_id
                    WHERE so.state = 'sale'
                )
                UNION
                (
                    SELECT pol.id * 2 + 1 AS id, po.date_order, po.name AS order_name, NULL AS sale_order_id, po.id AS purchase_order_id,
                    pol.partner_id, pol.company_id, pol.product_id,
                    com.sale_purchase_history_mode,
                    CASE com.sale_purchase_history_mode
                        WHEN 'qty_ordered' THEN pol.product_uom_qty
                        WHEN 'qty_rec_and_del' THEN pol.qty_received
                    END AS product_uom_qty,
                    pol.price_unit,
                    pol.discount,
                    CASE com.sale_purchase_history_mode
                        WHEN 'qty_ordered' THEN pol.price_subtotal
                        WHEN 'qty_rec_and_del' THEN pol.price_subtotal * pol.qty_received / NULLIF(pol.product_uom_qty, 0)
                    END AS price_subtotal,
                    po.currency_id, 'purchase' AS type, 0 as qty_delivered, pol.qty_received
                    FROM purchase_order_line pol
                    INNER JOIN purchase_order po ON pol.order_id = po.id
                    INNER JOIN res_company com ON com.id = pol.company_id
                    WHERE po.state IN ('purchase', 'done')
                )
            ''' % self._table)
    
    def action_sale_purchase_view(self):
        self.ensure_one()
        ret= {
                "name": (_("Order")),
                "type": "ir.actions.act_window",
                "view_mode": "form",
                "target": "current",
            }
        if self.type == "sale" and self.sale_order_id:
            ret.update({"res_model": "sale.order", "res_id": self.sale_order_id.id})
            return ret
        elif self.type == "purchase" and self.purchase_order_id:
            ret.update({"res_model": "purchase.order", "res_id": self.purchase_order_id.id})
            return ret
        return False
