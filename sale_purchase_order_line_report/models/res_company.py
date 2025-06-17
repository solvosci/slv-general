# © 2025 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    sale_purchase_history_mode = fields.Selection([
        ("qty_ordered", "Quantities ordered"),
        ("qty_rec_and_del", "Quantities received and delivered"),
    ], string="Sale/Purchase history mode", default="qty_ordered")
