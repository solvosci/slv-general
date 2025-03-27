# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class ResPartner(models.Model):
    _name = "res.partner"
    _inherit= ["res.partner", "sale.purchase.order.line.mixin"]

    def _get_action_view_domain(self):
        return [('partner_id','=',self.id)]
    
    def _get_action_view_context(self):
        ret = super()._get_action_view_context()
        ret.update({'hide_sale_purchase_partner': True})
        return ret
